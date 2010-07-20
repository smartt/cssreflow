
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
      --erik            Shortcut for flat with alphaprops, -alphaselectors, and line breaks between selector types.
      --flat            Puts declarations/rules on a single line.
      --help            Prints this Help message.
      --indent          Indent properties. [Default: on]
      --indentsize      Set the indent size. [Default: 2]
      --scan            Shortcut for silent, with warnings and errors displayed.
      --silent          Does not output the formatted text.
      --spaces          Use spaces to indent. [Default: on]
      --tabs            Use tabs to indent. [Default: off]
      --verbose         Output lots of information about the parsing process.
      --version         Print the version number of cssreflow being used.


Variable Substitution
---------------

CSSReflow 0.3 introduces basic variable substitution, allowing input CSS like this:

    /*
        @set my-background-color #06c
    */
    
    body {background-color: @my-background-color;}

The variable parser isn't very clever.  It looks for "@set KEY VALUE" patterns to setup a dictionary of user variables, then finds all "@KEY" strings and attempts to resolve the key by looking up it's value in the dictionary.  If the value isn't found, the @KEY statement will be left as-is.

If you're going to use this feature, put your @set definitions in a CSS comment.  Since all comments are removed before parsing, this will also remove the @set commands from the final output.

