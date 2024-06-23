# Misc - sh
Solved by **yappare**

## Question
Let's use JQ!

## Solution

By analysing the given source code (`main.py`), we can notice the input is vulnerable to some sort of injection due to no input sanitisation. However, it limits to maximum of 8 characters and denylist `;`, `&` and `|`.

```
@app.route("/", methods=["POST"])
def post():
    filter = request.form["filter"]
    print("[i] filter :", filter)
    if len(filter) >= 9:
        return render_template("index.tmpl", error="Filter is too long")
    if ";" in filter or "|" in filter or "&" in filter:
        return render_template("index.tmpl", error="Filter contains invalid character")
    command = "jq '{}' test.json".format(filter)
    ret = subprocess.run(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        encoding="utf-8",
    )
    return render_template("index.tmpl", contents=ret.stdout, error=ret.stderr)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)

```

By checking the official manual [here](https://jqlang.github.io/jq/manual/#invoking-jq), one of the ways that we can solve it by using `-f` argument.
>-f filename / --from-file filename:
>Read filter from the file rather than from a command line, like awk's -f option.

Hence, we could use the following payload,`'-f /f*'` which will make the full query as `jq '{' -f /f* '}' test.json`

### Flag
`FLAG{jqj6jqjqjqjqjqj6jqjqjqjqj6jqjqjq}`
