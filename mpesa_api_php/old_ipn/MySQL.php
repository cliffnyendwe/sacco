<?php
/**
* MySQL connection wrapper that uses the RAII idiom to manage connexions.
*/
class MySQL
{
   private $mysqli;
   
   public function __construct($host, $user, $pass, $db)
   {
       $this->mysqli = new mysqli($host, $user, $pass, $db);
   }

   public function __get($name)
   {
       return $this->$name;
   }

   function __destruct()
   {
       $this->mysqli->close();
   }
}
?>
