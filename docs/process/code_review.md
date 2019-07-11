# Code Review

The final step before merge into master and deploying is the code review.  This might be the most important step in the process so be diligent.

## Process

1. You will be notified of a pull request (PR) that has been assigned to you.  If you are assigned a pull request that you don't have time for or don't have the appropriate knowledge to handle let someone know immediately.

2. Ensure you don't have any changes to your current branch and switch to master.

        ➜  git:(whatever) ✗ git status
        On branch whatever 
        Your branch is up-to-date with 'origin/whatever'.
        ➜  git:(whatever) ✗ git checkout master
        Switched to branch 'master'
        Your branch is up-to-date with 'origin/master'.

3. Create a new branch and checkout the branch that you are reviewing.
        
        ➜  git:(master) ✗ git pull
        remote: Counting objects: 125, done.
        remote: Compressing objects: 100% (24/24), done.
        remote: Total 125 (delta 35), reused 110 (delta 15)
        Receiving objects: 100% (125/125), 1.25 MiB | 6.38 MiB/s, done.
        Resolving deltas: 100% (15/15), done.
           7e78acf..f1d04b1  master     -> origin/master
         * [new branch]      branch_to_review     -> origin/branch_to_review
        ➜  git:(master) git checkout origin/branch_to_review
        Branch branch_to_review set up to track remote branch branch_to_review from origin.
        Switched to a new branch 'branch_to_review'
        
4. Open your browser to the Github pull request page and the Github Issue associated with the pull request.  Read the requirements outlined in the Issue and ask questions of clarification to make sure you understand.

5. Run the unit tests and make sure they pass.  Also ensure new unit tests were created if appropriate.

6. "Smoke test" the changes.  Set up a simple use case (or a few) that will exercise the changes and make sure the behavior is what you expect.  This might include investigating values in the database, going to a web page and clicking around or a combination of both.

7. Once you are satisfied with the behavior check the code diff on Github.

    - Check for style
        - Does it follow PEP8?
        - Are the variables/methods/classes named appropriately (do the names make sense)?
        - Should it be broken up into multiple files?
        - Are the methods doing one and only one thing?
        - Are the methods easily testable (not too many decision branches)?
        - Is the code clear and readable?
        - Is the code well organized?
        - Do all methods return consistent types?
    - Check for efficiency and code optimizations
        - list comprehension vs. for loop
        - tuple vs. list
        - Are there possible problems if an incorrect type were to be used? (if such a scenario is possible)
        - Do all try/except conditions catch a specific exception type? (generic exception handling is not allowed)
    - Anything else that shouldn't be there?
        - Test code
        - Debug code
        - Print statements
        - TODOs
        - Typos
    - Anything else that should be there that isn't?
        - Missing unit tests?
        - Missing doc strings?
        - Missing coverage output?
        - Link to the Issue if necessary, to track requirements?

8. Ensure CI passes, if applicable.

    - Inspect logging for any issues that may have arisen from the package
    - Inspect any build failure and notify PR author
        
9. Make comments in the Github interface for any questions or suggestions along the way.  It's ok to provide encouragement here too!

    **If there are any problems along the way (unit tests don't pass, smoke test problem, etc) let the developer know and provide any info on how to reproduce the problem (including logs if necessary).**

10. If everything looks good to you, approve the pull request and notify the PR author to let them know it has been approved.
