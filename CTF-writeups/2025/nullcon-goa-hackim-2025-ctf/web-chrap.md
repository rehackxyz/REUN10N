# Solution
```
$MYPASSWORD = "AdM1nP@assW0rd!";
$target_crc16 = 25010;
$target_crc8 = 167;
$length = strlen($MYPASSWORD);
$charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()-_+=<>?';

function generate_password($length, $charset) {
    $password = '';
    $charset_length = strlen($charset);
    for ($i = 0; $i < $length; $i++) {
        $password .= $charset[rand(0, $charset_length - 1)];
    }
    return $password;
}

while (true) {
    $new_password = generate_password($length, $charset);
    if ($new_password !== $MYPASSWORD && crc16($new_password) === $target_crc16 && crc8($new_password) === $target_crc8) {
        echo "Found password: $new_password\n";
        break;
    }
}
```

password: `#V*-Ko<kwfiqGBt`
Flag: `ENO{Cr4hP_CRC_Collison_1N_P@ssw0rds!}`


Solved by: hikki
