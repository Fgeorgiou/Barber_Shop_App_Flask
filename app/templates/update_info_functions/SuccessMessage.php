<?php
//session start
session_start();
//DB connection
include '../includes/connection.php';

//check for open session else redirect
if(!isset($_SESSION['account_type'])){
    header("Location: Index.php");
}elseif(!isset($_POST['visitdate']) || !isset($_POST['visittime']) || !isset($_POST['personsoptions']) || !isset($_POST['smokers'])){
    header("Location: ReservationsTab.php");
}
//check for open session else redirect
if(!isset($_SESSION['account_type'])){
    header("Location: Index.php");
}

?>

<!-- This is the page that will inform the user that he succesfully changed a piece of personal information-->
<!DOCTYPE HTML>
<html lang="en">
    <head>
        <title>
            Success | Papa Felipe's®
        </title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- Bootstrap link to CSS & JavaScript -->
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>
        <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>
        <!-- Custom CSS & JavaScript -->
        <link rel="stylesheet" href="css/custom.css" type="text/css">
        <script src="js & jquery/myScripts.js"></script>
        <script src="js & jquery/jquery.js"></script>
        <script>
            window.setTimeout(function() {
            window.location = '../MyAccount.php';
            }, 3000);
        </script>        
        <!-- Background styling-->
        <style>
            .error {color: #FF0000;}
            
            body {
            background-image:    url(fonts/Background3t.jpg);
            background-attachment: fixed;
            }
        </style>
    </head>    
    
    <body>
    <!-- Success Message-->
    <div id="chgsuc" style="display:block">
            <div class="col-md-2"></div>
            <div class="col-md-8">
                <div class="alert alert-success text-centered">
                    Successful attempt to change your personal information. We are redirecting you back <?php echo $_SESSION['username'] . " " . $_SESSION['lname']; ?> !
                </div>
            </div>
            <div class="col-md-2"></div>
        </div>
    </body>
</html>
