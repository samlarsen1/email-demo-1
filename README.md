# email-demo-1

## Summary

Repo to prepare html content for use in models for AI templating.

Use this repo to convert `*.eml` files into HTML files with templated variables ready for freemaker

## Prerequisites

* `python3`

## How to run

Place `*.eml` files in the `./examples` folder and convert them to their `*.html` equivalent with personal attributes replaces. 

**Note**: *.eml files will not be added to git due to gitignore exclusions (eml will have personal identifiers in it).  Maintain a list of eml files outside the repo.

### Convert a single eml file to html

```python
# To convert an eml file to html with some personal identifiers replaced by freemaker templated variables
python3 extract_html.py \
    -i examples/lloyds/credit-card-eligibility.eml \
    -r "Mr Customer" "\${recipient.forename}" \
    -r "1234" "\${recipient.accountIdentifier}"
```

### Convert all eml files to html

Copy the `replacements.csv.example` file to `replacements.csv` and add your identifier replacements as space delimited key value pairs on each line (as shown in the example)

```bash
# Process all *.eml files under the examples/ folder
./process_emails.sh
```

### Clean up

`rm examples/*/*.html`