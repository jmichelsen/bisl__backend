# New Branch

When you make changes to the code base you will do it with branches.  The steps below will outline how to accomplish this and why it should be done.

## Process

1. **All** code changes should be the result of a story, task, or Issue (which one depend on your PM flow, but requirements should be tracked somewhere).  If you are making any code changes that are not associated with a story/task/Issue you should go create a story/task/Issue first.

2. Ensure your current branch is clean and then update your local master branch. Stash your changes if your branch is not clean.
        
        ➜  git:(master) ✗ git status
        On branch master
        Your branch is up-to-date with 'origin/master'.

        ➜  git:(master) ✗ git pull
        Current branch master is up to date.

2b. If your current branch is not clean, you can stash your current work to save for later if you are not in a place to commit what you are working on

        ➜  git:(doing_stuff) ✗ git status
        On branch doing_stuff
        Untracked files:
            (use "git add <file>..." to include in what will be committed)
            	new_dir/
        nothing added to commit but untracked files present (use "git add" to track)

        ➜  git:(doing_stuff) ✗ git stash
        Saved working directory and index state WIP on doing_stuff: 6aba6c6 Update something in master branch
        HEAD is now at 6aba6c6 Update something in master branch
        
        ➜  git:(doing_stuff) ✗ git checkout master
        Switched to branch 'master'
        Your branch is up-to-date with 'origin/master'.

        ➜  git:(master) ✗ git pull
        Current branch master is up to date.

3. Create a new branch that is named after the story/task/Issue, prefix with the issue number and add a description, ie issue457_optional_short_description, associated with this code change.

        ➜  git:(master) ✗ git checkout -b issue457__add_new_docs
        Switched to a new branch 'issue457__add_new_docs'
        ➜  git:(issue457__add_new_docs) ✗ 
    branch prefixes should help you identify the type of branch at a glance. 'issue', 'bugfix', or 'feature', are acceptable prefixes.

4. Design discussion.  If the story you are working on has any level of complexity, or if you are unsure about how to implement the change, request a design meeting with a fellow developer to discuss how to get started.  It's *much* better to take 30 minutes talking about this up front than to spend 6 hours having to refactor your entire design after a code review.

5. Be sure to periodically (once daily before you begin working) merge master *into* your working branch.  This helps keep minimize the risk of merge conflicts while developing your code.

        ➜  git:(issue457__add_new_docs) ✗ git fetch origin
        ➜  git:(issue457__add_new_docs) ✗ git merge origin/master
        Already up-to-date.
        
**Do not accidentally merge your branch into master!  This is VERY important.**

The `git merge {target}` command takes the target branch and merges it into the branch _you are currently on_
