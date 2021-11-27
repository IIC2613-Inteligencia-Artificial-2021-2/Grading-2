#!/usr/bin/env fish

function setup
  echo "  * Setting up assignment directory"
  if test -f $argv/.envrc
    echo "    - Moving .envrc and shell.nix"
    mv $argv/.envrc{,.bak}
    mv $argv/shell.nix{,.bak}
  end
end

function grade
  echo "  * Grading"

  # rm -rf $argv/test_results
  # set_color red
  # echo "    - WARNING: Removing old test results while developing"
  # set_color normal

  if test -d $argv/test_results
    echo "    - Test result directory exists, not touching it..."
    return
  end

  mkdir $argv/test_results
  mkdir $argv/test_results/passed
  mkdir $argv/test_results/failed
  mkdir $argv/test_results/logs

  echo "    - Running tests"

  echo "      - Constraint Satisfaction"
  set_color blue
  echo "        - Dependency Hell"
  set_color normal
  ./dh.py \
    --assignment_dir $argv \
    --instances_dir ./tests/csat/dep_hell/instances \
    --output_name dh \
    --output_dir $argv/test_results/ \
    --base_files $argv/csat/dep_hell/dh.lp

  echo "      - Planning"
  set_color blue
  echo "        - Statues"
  set_color normal
  ./statues.py \
    --assignment_dir $argv \
    --instances_dir ./tests/planning/statues/instances \
    --output_name statues \
    --output_dir $argv/test_results/ \
    --base_files $argv/planning/strips.lp \
                 $argv/planning/statues/statues.lp

  set_color blue
  echo "        - Blocks-world single-agent"
  set_color normal
  ./blocks.py \
    --assignment_dir $argv \
    --instances_dir ./tests/planning/blocks/simple/instances/ \
    --output_name blocks-simple \
    --output_dir $argv/test_results/ \
    --single_agent \
    --base_files $argv/planning/strips.lp \
                 $argv/planning/blocks/blocks.lp
  set_color blue
  echo "        - Blocks-world multi-agent"
  set_color normal
  ./blocks.py \
    --assignment_dir $argv \
    --instances_dir ./tests/planning/blocks/multi/instances/ \
    --output_name blocks-multi \
    --output_dir $argv/test_results/ \
    --base_files $argv/planning/strips-multiagent.lp \
                 $argv/planning/blocks/blocks-multiagent.lp

  set_color blue
  echo "        - Coffee single-agent"
  set_color normal
  ./coffee.py \
    --assignment_dir $argv \
    --instances_dir ./tests/planning/coffee/simple/instances/ \
    --output_name coffee-single \
    --output_dir $argv/test_results/ \
    --single_agent \
    --base_files $argv/planning/strips.lp \
                 $argv/planning/coffee/coffee.lp
  set_color blue
  echo "        - Coffee multi-agent"
  set_color normal
  ./coffee.py \
    --assignment_dir $argv \
    --instances_dir ./tests/planning/coffee/multi/instances/ \
    --output_name coffee-multi \
    --output_dir $argv/test_results/ \
    --base_files $argv/planning/strips-multiagent.lp \
                 $argv/planning/coffee/coffee-multiagent.lp
end


for assignment_directory in $argv
  echo "Grading $assignment_directory"
  setup $assignment_directory

  grade $assignment_directory
  echo ""
end
