### Understanding the code

Read the files in this order:

1. data_structures.py
2. listcheen.py
3. go.py

### Adding a criterion

1. Add it in `./initial_data/criteria.json`
2. If it's constant value add its values as a new file in `./initial_data/constant_values` or if it's dependant on the user input, add it in `./user_input/values/`. The name should be `<criterion_name>.json` and the content should be a dict of rows (unis or fields or programs or general options) to values.
3. Add it's user weights in `./user_input/weights.json`
