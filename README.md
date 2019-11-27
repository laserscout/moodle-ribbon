# Ribbon <br/> Parametric variation of a moodle quiz #

We introduce `Ribbon` a wrapper around Moodle’s `GIFT` format, which enables instructors to compose a quiz in a `Markdown` document, with questions that have multiple versions. The tool accepts templated questions with placeholder strings in the body of the question and a list of multiple values, or a function/routine that generates a list of values. The output is a `GIFT` file containing a question for each variation of the list. This reduces the amount of time needed to create a high quality exam while minimizing students' incentive for copying each other.

## Prerequisites

The only dependency of the `Ribbon` module is `Python 3`. All imported packages should be installed in a clean, new `Python 3` installation.

## Usage

Usage information and help is include within the script. Issue

```bash
python3 ribbon.py --help
```

for command line options and documentation.

## Example

Using the `csv` comment block, you can generate a question template, where the variables will be substituted by `Ribbon` to generate the final `GIFT` questions.  Each template can have a header name, which identifies the hierarchy in the moodle question bank. The example

     # exam/text/substitution
     <!-- csv
     form           , word       , answer
     past tense     , run        , ran
     plural         , mouse      , mice
     scientific term, yawning    , oscitancy
     Latin term     , unconquered, invicta
     -->
     The {{form}} of {{word}} is { ={{answer}} }

will generate 4 questions based on the template, with names Q001, ..., Q004 under exam/text/substitution path in moodle question bank.

## Contributors 

*Design and development*:\
Frank Blanning<sup>1</sup>,
Dimitris Floros<sup>1</sup>,
Nikos Pitsianis<sup>1</sup>, 

*Acknowledgements*:\
We thank Xiaobai Sun<sup>2</sup> for her critical comments

<sup>1</sup> Department of Electrical and Computer Engineering,
Aristotle University of Thessaloniki, Thessaloniki 54124, Greece\
<sup>2</sup> Department of Computer Science, Duke University, Durham, NC
27708, USA
