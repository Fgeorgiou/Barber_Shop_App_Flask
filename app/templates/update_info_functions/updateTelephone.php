<?php
//This page will offer the options of editing one's Telephone.
//It is available to every user
//session start
session_start();
//DB connection
include '../includes/connection.php';

//check for open session else redirect
if(!isset($_SESSION['account_type'])){
    header("Location: Index.php");
}

//declaring variables
$sessionId = $_SESSION['userid'];
$sqltelephone = $_SESSION['userTelephone'];
$telephone = " ";
$telErr = $telErr1 = $telErr2 = " ";

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    //email validation
    if(empty($_POST["telold"]) || empty($_POST["tel1"])){
        $telErr= "Telephone is required";
    }
    elseif(test_input($_POST["tel1"]) !== test_input($_POST["tel2"])){
        $telErr1 = "Telephone numbers inserted do not match! ";
    }
    else{
        $telephone = test_input($_POST["tel1"]);
        if (!preg_match('/^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$/',$telephone)) { 
            $telErr2 = "Invalid telephone format (invalid characters)";      
        } else if(strlen($telephone) < 10)
            {
                $telErr2 = "Invalid telephone format (telephone too short)";
            }
    }
}

if(isset($_POST["tel1"]) && isset($_POST["tel2"]) && $telErr === " " && $telErr1 === " " && $telErr2 === " "){
    $sql = "UPDATE users SET telephone = '$telephone' WHERE telephone = '$sqltelephone' AND userid = '$sessionId'";
        $result = mysqli_query($conn,$sql);
            if ($result === TRUE) {
                $_SESSION['userTelephone'] = $telephone;
                header("Location:SuccessMessage.php");
            }
} 
$conn->close();

//function for filtering data from extra whitespaces, slashes and translating html special characters to harmless text
function test_input($data) {
  $data = trim($data);
  $data = stripslashes($data);
  $data = htmlspecialchars($data);
  return $data;
}

?>

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
        <link rel="stylesheet" href="../css/custom.css" type="text/css">
        <script src="../js & jquery/myScripts.js"></script>
        <script src="../js & jquery/jquery.js"></script>
        <style>
            body {
            background-image:    url(../fonts/background3t.jpg);
            background-attachment: fixed; 
            }
        </style>
    </head>
    
   
   
    <body class="img-responsive">
        
    <!--Navigation bar 1.7 -->
    <!-- Reference: W3Schools http://www.w3schools.com/bootstrap/bootstrap_navbar.asp-->
        <nav class="navbar navbar-default">
            <div class="container-fluid">
                <div class="navbar-header">
                    <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#myNavbar">
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>
                        <span class="icon-bar"></span>                         
                    </button>
                    <a class="navbar-brand hidden-lg hidden-md" href="../Customer_Interface.php"><span class="glyphicon glyphicon-home"></span></a>
                    <a class="navbar-brand hidden-sm hidden-xs" href="../Customer_Interface.php"><span id="logo">Papa Felipe's</span></a>
                </div>
                <div class="collapse navbar-collapse" id="myNavbar">
                    <ul class="nav navbar-nav">
                        <li><a href="../Menu.php">Menu</a></li>
                        <li><a href="../ReservationsTab.php">Reservations</a></li>
                        <li><a href="../Contact.php">Contact</a></li>
                        <li><a href="../AboutUs.php">About Us</a></li>
                    </ul>   
                    <ul class="nav navbar-nav navbar-right navbar-collapse" style="font-size:calc(80% + 1vw); position: relative; top:2%;">
                        <div class="dropdown">
                            <span class="glyphicon glyphicon-cog dropdown-toggle" data-toggle="dropdown"><?php echo $_SESSION['username'];?></span>
                            <span class="caret"></span>
                        <ul class="dropdown-menu">
                            <li><a href="../MyAccount.php"><span class="glyphicon glyphicon-user"></span> My Account</a></li>
                            <?php if($_SESSION['account_type'] === "admin") { ?> <li><a href="../Admin_Interface.php"><span class="glyphicon glyphicon-king"></span> Admin Interface</a></li> <?php } ;?>
                            <li><a href="../Logout.php"><span class="glyphicon glyphicon-log-in"></span> Logout</a></li>
                        </ul>
                        </div>
                    </ul>
                </div>
            </div>
        </nav>            
        
    <!-- End of navigation bar -->
    
    
    <!-- Content-->
    <!--Form--> 
        <div class="row">    
            <div class="col-sm-4"></div>
            <div class="col-sm-4">
                <div class="wrapper2">
                <form action="<?php echo htmlspecialchars($_SERVER["PHP_SELF"]); ?>" method="post">
                    <div class="form-group">
                        <label for="telold"><b>Currently Used Telephone Number:</b></label>
                        <input type="text" class="form-control" name="telold">
                        <span class="error"><?php echo $telErr;?></span>
                    </div>
                    <div class="form-group">
                        <label for="tel1"><b>New Telephone Number:</b></label>
                        <input type="text" class="form-control" name="tel1">
                        <span class="error"><?php echo $telErr . $telErr1;?></span>
                    </div>
                    <div class="form-group">
                        <label for="tel2"><b>Repeat New Telephone Number:</b></label>
                        <input type="text" class="form-control" name="tel2">
                        <span class="error"><?php echo $telErr2;?></span>
                    </div>
                    <button type="submit" class="btn btn-default">Submit</button>
                </form>                                                                                                                          
            </div>
            <div class="col-sm-4"></div>
        </div>

        </div>
    </body>
</html> 