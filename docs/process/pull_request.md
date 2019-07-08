# Pull Requests

All contributions to the project will go through a merging process.  Below are the steps necessary before code can be added to the master branch and deployed to production.

## Process

1. Before creating a pull request, ensure that your code has passed any QA tests and has been approved for production.

2. Test locally:

    - Did you write new unit tests for the applicable additions for this merge?
    - Did you "smoke" test before creating the pull request?
    - Do *all* unit tests pass?
    - Does CI pass?
        
3. Create a pull request in Github.

    - Add details to the description of the pull request.  This should **always** include a link to the issue/story/task associated with the pull request (put this as the first line). If issues are tracked in github, this is unnecessary.
    - Include a description of the urgency of the pull request.
        - Low: A cosmetic update (code typo, doc string formatting, etc)
        - Medium: This would let the reviewer know they should set aside some time between now and the next work day to do the code review.  (Most pull requests fall into this category)
        - High: Needs immediate attention.  Drop everything you are doing.  All hands on deck.  (This would ideally never occur.)
    - Copy a link of the pull request into the issue/story/task as a comment for reverse reference. (optional for Github tracked Issues)
    - Assign the pull request to a team member who is available and appropriate.  Notify this person via chat to ensure they are aware of their new assignment.  Be sure to make them aware of the urgency.
    - Upon the successful completion of a code review, you will be notified that the merge is approved.

5. Once the PR has been approved, plan a a time for deployment

    - Determine an appropriate time and day to deploy - **right now** might not be the best time
    - When you are ready to deploy, merge the branch into master (using the Github UI)
    - Go through the necessary steps to deploy to production. (CI/CD makes this step irrelevant)
    - Do not delay deployment once the branch has been merged. Deploying multiple changes in a single deploy makes troubleshooting any problems more difficult.
