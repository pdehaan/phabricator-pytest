"""
https://wiki.mozilla.org/Phabricator/TestPlan
"""

import os
# import subprocess

import dotenv
# import requests
import hgapi
import pytest
from pytest_bugzilla_notifier.bugzilla_rest_client import BugzillaRESTClient

CONF = dotenv.find_dotenv()
if CONF:
    dotenv.load_dotenv(CONF)

BUGZILLA_CLIENT = BugzillaRESTClient({
    'bugzilla_host': os.getenv('BUGZILLA_HOST'),
    'bugzilla_api_key': os.getenv('BUGZILLA_API_KEY_1')
})

repo = hgapi.Repo("peter")

def run_cmd(cmd_arr):
    """ Run a command using subprocess. """
    output = ' '.join(cmd_arr)
    return dict(stdout=output)
    # return subprocess.run(cmd_arr, capture_output=True, text=True, check=True)


class TestPlan():
    """ Run all the tests! """

    @pytest.mark.skip(reason="Potential Selenium test")
    def test_t1_signing_up_is_successful(self):
        """
        NOTES: dkl and I flagged this as a potential Selenium test.

        # I'm not sure this is possible. I tried on dev and don't get confirmation emails when
        # creating a new account. I tried using Puppeteer and verifying via the UI in Chromium,
        # but when I try and log into Phabricator with my new, verified Bugzilla account, it tells
        # me I need 2FA, which breaks my automation plan.
        """

        """
        # T1 - Signing up is successful

        ## Test Plan
        1. Create a new BMO account.
        2. Make sure to include an irc nick in the Real Name field.
            - E.g. "John Doe [:jdoe]"
        3. Go to Phabricator and login as the new user.
        4. Finish account creation.

        ## Results
        1. After logging into Phabricator, on the "Create a New Account" page,
            1. Username should be prefilled with the irc nick,
            2. Real Name is correct and does not contain [] or any other extraneous characters.
        2. Clicking register approval completes account creation without error.
        3. The account works as expected.
        """
        
        return


    def test_t2_creating_a_revision_is_successful(self):
        """
        NOTES:
        - not sure how to automate a test which would bypass triaging (per step 1)
        - this requires the test to be run in a specific directory with existing repo files (step 2)
        - need to verify if the bugzilla Python script returns the phabricator revision information in the JSON response.
        - need to figure out how to verify the author received an email (which is possible via restmail, but requires explicitly creating a restmail account which could be tricky since anybody can access the inbox and do password change, etc.)
        """

        """
        # T2 - Creating a revision is successful

        NOTE: Make sure you have `moz-phab` properly setup on your machine and have run `arc install-certificate` using the Phabricator user you wish to test with as documented above.

        ## Test Plan
        1. Go to BMO and create a new bug as the Bugzilla user that the Phabricator account is connected to. (Or use an existing public bug).
            - To create bugs directly and bypass triaging, go to https://bugzilla.allizom.org/enter_bug.cgi?product=Firefox&format=__default__ (staging) or https://bugzilla-dev.allizom.org/enter_bug.cgi?product=Firefox&format=__default__ (dev)
        2. Using the repo listed in the "Getting Started" section above that matches the environment you are testing, make some change to a file.
        3. Run `hg commit -A -m 'Bug <bug_id>: New changes'`
        4. Run `moz-phab`

        ## Results
        1. `moz-phab` only submitted the 1 newly created commit.
        2. Visit Phabricator and there should be a new revision with the title.
        3. The revision should contain the correct diff of the changes that were made.
        4. The "Bugzilla Bug ID" is correct.
            1. The Bug number is correct.
            2. The link is correct based on the environment (bugzilla.allizom.org for staging, bugzilla-dev.allizom.org for dev).
            3. If the bug in Bugzilla is a public bug, the revision should also be public.
        5. Visiting the bug on Bugzilla shows an entry for the new revision in the Phabricator Revisions section.
        6. Author received an email from mozphab-dev@mozilla.com. It has a title formatted as "[Differential] [Changed Policy] D{revision number}: {first line}." and a body with a text "phab-bot changed the visibility from "Administrators" to "Public (No Login Required)"."
        """

        """ Step 1. """
        bug_data = {
            'product': 'Firefox',
            'component': 'Developer Tools',
            'summary': 'Test Bug',
            'version': 'unspecified'
        }
        bug_id = BUGZILLA_CLIENT.bug_create(bug_data)

        """ Step 3. """
        try:
            repo.hg_commit(f"'Bug {bug_id}: New changes'", amend=True)
        except hgapi.HgException as err:
            print(err)
            pass

        """ Step 4. """
        mozphab_output = run_cmd(["moz-phab"])
        print(mozphab_output)

        return

    @pytest.mark.skip(reason="hg_commit requires positional argument: 'reference'")
    def test_t3_updating_a_revision_with_an_ammended_commit_is_successful(self):
        """
        # T3 - Updating a revision with an amended commit is successful

        ## Test Plan
        1. `hg update` to a commit which you previously submitted with `moz-phab`
        2. Make a change and run `hg commit --amend`
        3. Run `moz-phab`

        ## Results
        1. `moz-phab` should automatically detect a current revision and update it.
        2. The revision is updated with the new diff on Phabricator:
            1. The History tab should have two entries, Diff 1 and Diff 2.
            2. The Commits tab should have a single entry.
        3. The bug id and other information remains unchanged.
        """

        """ Step 1. """
        # TypeError: hg_update() missing 1 required positional argument: 'reference'
        # repo.hg_update()

        """ Step 2. """
        try:
            repo.hg_commit("commit msg", amend=True)
        except hgapi.HgException as err:
            print(err)
            pass

        """ Step 3. """
        mozphab_output = run_cmd(["moz-phab"])
        print(mozphab_output)

        return

    """
    QUESTIONS:
    - not sure how to set security-sensitive boxes via Python API. Or if this is better/possible in Bash script.
    """
    def test_t4_creating_a_secure_revision_is_successful(self):
        """
        # T4 - Creating a secure revision is successful

        NOTE: Your Bugzilla user must belong to a security group, e.g. core-security.

        ## Test Plan
        1. Go to bugzilla and create a security bug:
        2. Click "Edit Bug", open the "Security" panel, and check one of the security-sensitive boxes, e.g. "Security-Sensitive Core Bug".
        3. Run `hg commit -A -m 'Bug <bug_id>: Private changes'`
        4. Run `moz-phab`.

        ## Results
        1. The diff and information of the revision are as expected.
        2. The revision has a "Custom Policy" attached to it.
        3. Click "Edit Revision" and then click on the "Visible To" drop down, and select the "Custom Policy" choice.
        4. It should read "Allow members of projects", followed by the names of projects corresponding to all Bugzilla groups the private bug is categorized under. For example, a bug private to core-security, should have the project name "bmo-core-security".
        5. The revision has a "secure-revision" project tag added.
        6. The revision has a warning titled "This is a secure revision.".
        7. The revision added the creator as a subscriber.
        8. The revision is visible to the user who made it.
        9. The revision is visible to users belonging to the security groups of the bug.
        10. Visiting the bug on Bugzilla shows an entry for the new revision in the Phabricator Revisions section with summary as '(secure)'.
        11. The revision is NOT visible to the public without logging in.
        12. The revision is NOT visible to logged in members without the correct permission.
        """

        """ Step 1. """
        bug_data = {
            'product': 'Firefox',
            'component': 'Developer Tools',
            'summary': 'Test Secure Bug',
            'version': 'unspecified',
            'groups': ['firefox-core-security']
        }
        bug_id = BUGZILLA_CLIENT.bug_create(bug_data)

        """ Step 3. """
        try:
            repo.hg_commit(f"'Bug {bug_id}: Private changes'", amend=True)
        except hgapi.HgException as err:
            print(err)
            pass

        """ Step 4. """
        mozphab_output = run_cmd(["moz-phab"])
        print(mozphab_output)

        return

    """
    QUESTIONS:
    - same as above. needs access to email w/ API to verify the user got the expected emails
    """
    def test_t5_adding_a_secure_bug_to_an_existing_revision_locks_it_down(self):
        """
        # T5 - Adding a secure bug to an existing revision locks it down

        NOTE: Your Bugzilla user must belong to a security group, e.g. core-security. You will also need a second, unprivileged user.

        ## Test Plan
        1. Go to bugzilla and create a public bug:
        2. Run `hg commit -A -m 'Bug <bug_id>: Public changes'`
        3. Run `moz-phab`.
        4. Check if revision is available for public.
        5. Go to bugzilla and create a security bug:
        6. Click "Edit Bug", open the "Security" panel, and check one of the security-sensitive boxes, e.g. "Security-Sensitive Core Bug".
        7. Edit the revision created above, and set the Bugzilla Bug ID field to the ID of the newly created private bug.
        8. Add the second, unprivileged Bugzilla user to the bug's CC list.

        ## Results
        1. The revision has a "Custom Policy" attached to it.
        2. Click "Edit Revision" and then click on the "Visible To" drop down, and select the "Custom Policy" choice.
        3. It should read "Allow members of projects", followed by the names of projects corresponding to all Bugzilla groups the private bug is categorized under. For example, a bug private to core-security, should have the project name "bmo-core-security".
        4. The revision has a "secure-revision" project tag added.
        5. The revision has the creator and the second Bugzilla user as subscribers.
        6. The revision is visible to the user who made it.
        7. The revision is visible to users belonging to the security groups of the bug.
        8. The revision is NOT visible to the public without logging in.
        9. The revision is NOT visible to logged in members without the correct permission.
        10. The revision IS visible to the second Bugzilla user.
        11. Visiting the bug on Bugzilla shows an entry for the new revision in the Phabricator Revisions section.
        12. The reviewer received an email from the author with a text "The content for this message can only be transmitted over a secure channel." and a link to Phabricator.
        """

        """ Step 1. """
        bug_data = {
            'product': 'Firefox',
            'component': 'Developer Tools',
            'summary': 'Test Public Bug',
            'version': 'unspecified'
        }
        bug_id = BUGZILLA_CLIENT.bug_create(bug_data)

        """ Step 2. """
        try:
            repo.hg_commit(f"'Bug {bug_id}: Public changes'", amend=True)
        except hgapi.HgException as err:
            print(err)
            pass

        """ Step 3. """
        mozphab_output = run_cmd(["moz-phab"])
        print(mozphab_output)

        return

    def test_t6a_creating_a_revision_checks_the_bug_id(self):
        """
        # T6a - Creating a revision checks the bug id

        ## Test Plan
        1. Entering an invalid bug id, e.g "abcd efg" or "$1000", fails.
        2. Run `hg commit -A -m 'Bug <bug_id>: Public changes'`
        3. Run `moz-phab`.

        ## Results
        1. Entering an invalid bug id, e.g "abcd efg" or "$1000", fails.
        """

        """ Step 2. """
        invalid_bug_id = "abcd efg"
        repo.hg_commit(f"'Bug {invalid_bug_id}: Public changes'", amend=True)

        """ Step 3. """
        mozphab_output = run_cmd(["moz-phab"])
        print(mozphab_output)

        return

    def test_t6b_creating_a_revision_checks_the_bug_id(self):
        """
        # T6b - Creating a revision checks the bug id

        ## Test Plan
        1. Entering the id of a bug that does not exist fails.
        2. Run `hg commit -A -m 'Bug <bug_id>: Public changes'`
        3. Run `moz-phab`.

        ## Results
        1. Entering the id of a bug that does not exist fails.
        """

        """ Step 2. """
        try:
            bug_id = 9999
            repo.hg_commit(f"'Bug {bug_id}: Public changes'", amend=True)
        except hgapi.HgException as err:
            print(err)
            pass
        except AssertionError as err:
            print(err)
            pass
        else:
            print("Unexpected passing test")

        """ Step 3. """
        mozphab_output = run_cmd(["moz-phab"])
        print(mozphab_output)

        return

    def test_t6c_creating_a_revision_checks_the_bug_id(self):
        """
        # T6c - Creating a revision checks the bug id

        ## Test Plan
        1. Entering the id of a bug of a secure revision that the user does not have access to fails.
        2. Run `hg commit -A -m 'Bug <bug_id>: Public changes'`
        3. Run `moz-phab`.

        ## Results
        1. Entering the id of a bug of a secure revision that the user does not have access to fails.
        """

        """ Step 2. """
        try:
            secure_bug_id = 1395350
            repo.hg_commit(f"'Bug {secure_bug_id}: Public changes'", amend=True)
        except hgapi.HgException as err:
            print(err)
            pass

        """ Step 3. """
        mozphab_output = run_cmd(["moz-phab"])
        print(mozphab_output)

        return

    def test_t6d_creating_a_revision_checks_the_bug_id(self):
        """
        # T6d - Creating a revision checks the bug id

        ## Test Plan
        1. Entering a valid bug id is successful.
        2. Run `hg commit -A -m 'Bug <bug_id>: Public changes'`
        3. Run `moz-phab`.

        ## Results
        1. Entering a valid bug id is successful.
        """

        """ Step 2. """
        try:
            bug_id = 9999
            repo.hg_commit(f"'Bug {bug_id}: Public changes'", amend=True)
        except hgapi.HgException as err:
            print(err)
            pass

        """ Step 3. """
        mozphab_output = run_cmd(["moz-phab"])
        print(mozphab_output)

        return

    def test_t7_creating_multiple_revisions_with_the_same_bug_id_is_successful(self):
        """
        # T7 - Creating multiple revisions with the same bug id is successful

        ## Test Plan
        1. Run `hg commit -A -m 'Bug <bug_id>: Public changes'`
        2. Run `moz-phab`.
        3. Create a different comment using same bug id but different title.

        ## Result
        1. Both revisions are created successfully.
        2. Visiting the bug on Bugzilla shows 2 corresponding entries for the revisions in the Phabricator Revisions section.
        """

        bug_id = 9999

        """ Step 1. """
        try:
            repo.hg_commit(f"'Bug {bug_id}: Public changes'", amend=True)
        except hgapi.HgException as err:
            print(err)
            pass

        """ Step 2. """
        mozphab_output = run_cmd(["moz-phab"])
        print(mozphab_output)

        """ Step 3. """
        try:
            repo.hg_commit(f"'Bug {bug_id}: More public changes'", amend=True)
        except hgapi.HgException as err:
            print(err)
            pass

        mozphab_output2 = run_cmd(["moz-phab"])
        print(mozphab_output2)

        return

    def test_t8_requesting_and_leaving_a_review_on_a_revision_is_successful(self):
        """
        # T8 - Requesting and leaving a review on a revision is successful

        NOTE: Ensure that you have 2 Phabricator accounts that log in via Bugzilla ready to go.

        ## Test Plan
        1. Create a commit with other account as reviewer using `hg commit -m 'Bug <bug_id>: New changes r?<reviewer>'`.
        2. Run `moz-phab`.
        3. Log into Phabricator as the reviewer account.
        4. Add the "Accept Revision" action at the bottom. Submit.
        5. Add the "Request Changes" action at the bottom. Submit.

        ## Results
        1. The Phabricator revision is visible in the Bugzilla bug.
        2. Reviewer received an email from author with a text "{author} added a reviewer: {reviewer}"
        3. Author received an email from reviewer with a text "{reviewer} accepted this revision."
        4. Author received an email from reviewer with a text "{reviewer} requested changes to this revision."
        """

        """ Step 1. """
        bug_id = 0000
        reviewer = "johndoe"
 
        try:
            repo.hg_commit(f"'Bug {bug_id}: New changes r?{reviewer}'", amend=True)
        except hgapi.HgException as err:
            print(err)
            pass

        """ Step 2. """
        mozphab_output = run_cmd(["moz-phab"])
        print(mozphab_output)

        return

    @pytest.mark.skip(reason="Potential Selenium test")
    def test_t9_abandoning_a_revision_obsoletes_the_attachment(self):
        """
        # T9 - Abandoning a revision obsoletes the attachment

        ## Test Plan
        1. On a previously created revision, perform the "Abandon Revision" action from the "Add Action" dropdown.

        ## Results
        1. The bug shows the revision as 'Abandoned' in the Phabricator Revisions list of the bug.
        2. The bug history shows the attachment is being set to obsolete.
        """

        return

    @pytest.mark.skip(reason="Potential Selenium test")
    def test_t10_reclaiming_a_revision_unobsoletes_the_attachment(self):
        """
        # T10 - Reclaiming a revision unobsoletes the attachment

        ## Test Plan
        1. In the revision used as part of the "Abandoning a revision obsoletes the attachment" test (T9), perform the "Reclaim revision" action.

        ## Results
        1. The bug's Phabricator attachment is unobsoleted and the revision is not abandoned any longer in the Phabricator revisions list.
        """

        return

    def test_t11_creating_a_diff_from_local_git_repository_to_remote_mercurial_repository_is_not_allowed(self):
        """
        # T11 - Creating a Diff from local git repository to remote Mercurial repository is not allowed

        ## Test Plan
        1. Change directory to the repository *phabricator-qa-dev-cinnabar*.
        2. Create a commit with git and run `arc diff`.
        3. Fill the needed data (Test Plan) and confirm.

        ## Results
        1. Creating a diff fails with :
            > ERR-CONDUIT-CORE: Local VCS (git) is different from the remote repository VCS (hg).
        """

        # Not sure how we can change the directory into new repo, or if this is some other test dir structure.

        """ Step 2. """
        hg_output = run_cmd(["arc", "diff"])
        print(hg_output)

        return

    def test_t12_patching_diff_created_from_git_repository(self):
        """
        # T12 - Patching Diff created from git repository

        ## Test Plan
        1. Using a commit created above run `cinnabarrc diff HEAD~`.
        2. Fill the needed data (Test Plan) and confirm.
        3. Change directory to *phabricator-qa-dev*.
        4. Run `moz-phab patch D{number of the revision created above}`.

        ## Results
        1. Code is sucessfully patched using the Diff.
        """

        # Depends on previous test, "T11".

        """ Step 1. """
        hg_output = run_cmd(["cinnabarrc", "diff", "HEAD~"])
        print(hg_output)

        """ Step 4. """
        revision_id = "number of the revision created above"
        mozphab_output = run_cmd(["moz-phab", "patch", f"D{revision_id}"])
        print(mozphab_output)

        return

    @pytest.mark.skip(reason="Potential Selenium test")
    def test_t13_verify_the_private_revisions_deliver_emails_that_does_not_contain_any_sensitive_content(self):
        ## NOT SURE HOW TO DO THE INITIAL STEPS. THIS ALMOST SEEMS BETTER AS A E2E test using Puppeteer or Selenium
        ## IF WE MEED TO DO A LOT OF UI INTERACTIONS (UNLESS THERE ARE "Self Action > Enable Self Action Mail" CONFIGS
        ## VIA THE API.
        ## The other consideration will be verifying the received email, which may require some special @restmail.net
        ## account which will let us query the inbox and validate the title/summary/text/etc. But not sure if that will
        ## be a security concern since there is no access control around who can access @restmail.net emails (which could
        ## mean that people could change the passwords and log in as our test user).

        """
        # T13 - Verify the private revisions deliver emails that does not contain any sensitive content

        NOTE: Your Bugzilla user must belong to a security group, e.g. core-security.

        ## Test Plan
        1. Login to Phabricator (after creating account in Bugzilla) using an account that can have email delivered to it, such as your own email address.
        2. At the top right of Phabricator, click on your initial or gravatar image to open the drop down menu and select "Settings".
        3. Click on "Email Delivery".
        4. Select "Enable Self Action Mail" for the "Self Action" drop down.
        5. Click "Save Changes".
        6. Go to Bugzilla and create a security bug:
            - Click "Edit Bug", open the "Security" panel, and check one of the security-sensitive boxes, e.g. "Security-Sensitive Core Bug".
        7. Create a new hg commit.
        8. Run `moz-phab`.

        ## Results
        1. The diff and information of the revision are as expected.
        2. The revision has a "Custom Policy" attached to it.
        3. The revision has a "secure-revision" project tag added.
        4. The revision has a warning titled "This is a secure revision".
        5. Check to see if you received an email about the new object (Revision) that was just created.
        6. The email should not contain any information about the revision other than a link to Phabricator.
        7. Clicking on the link in the email should take you to the Phabricator page that displays the full unfiltered email contents.
        8. The email contents should contain the title, summary, test plan, reviewers, etc. of the new revision.
        9. Submitting a public revision should instead show the full contents in the email similar to what was displayed on the Phabricator mail page.

        ## Step 7.
        # bug_id = 9999
        # hg_output = run_cmd(
        #     ["hg", "commit", "-A", "-m",
        #      f"'Bug {bug_id}: New changes'"]
        # )
        # print(hg_output)

        ## Step 8.
        # mozphab_output = run_cmd(["moz-phab"])
        # print(mozphab_output)
        """

        return
