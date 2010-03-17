
CSSReflow
=========

CSSReflow is a CSS formatter/beautifier. It was written to clean-up existing CSS files (useful when inheriting someone else's markup.)  It's written in Python, and expected to be run from the command-line (for now.)


Usage
-----

    cssreflow.py INPUT-FILE [OPTIONS] > OUTPUT-FILE
    
    Options:
    
      --alphaprops      Alphabetizes the CSS properties. [Default: off]
      --alphaselectors  Alphabetizes the CSS selectors (potentially altering inheritence rules.) [Default: off]
      --clean           Shortcut for 2-space indent with alpha-props.
      --erik            Shortcut for flat with alpha-props and selectors.
      --flat            Puts declarations/rules on a single line.
      --help            Prints this Help message.
      --indent          Indent properties. [Default: on]
      --indentsize      Set the indent size. [Default: 2]
      --scan            Shortcut for silent, with warnings and errors displayed.
      --silent          Does not output the formatted text.
      --spaces          Use spaces to indent. [Default: on]
      --tabs            Use tabs to indent. [Default: off]
      --version         Print the version number of cssreflow being used.

