
Steps to push github
====================

.. list-table::
   :widths: 20 80
   :header-rows: 1
   
   * - STEPs
     - Operations
   * - STEP0
     - run "python manage.py test" to make sure all things works well
   * - STEP 1
     - git checkout -b <your_new_branch>
   * - STEP 2
     - code your task
   * - STEP 3
     - git commit -a
   * - STEP 4
     - repeat STEP2-3 until your task locally finish 
   * - STEP 5
     - git pull --rebase origin master
   * - STEP 6
     - git push origin HEAD
   * - STEP 7
     - pull request on github
   * - STEP 8
     - Assign to someone to review
   * - STEP 9
     - Modified as SomeOne Comment
   * - STEP 10
     - Go back to STEP5 until finally merged
   * - STEP 11
     - git checkout -b <next_task_branch>


.. note:: Delete your master branch if you still keep it any time! 
