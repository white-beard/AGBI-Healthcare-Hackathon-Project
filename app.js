let express = require("express"),
    port = process.env.PORT || 3000,
    bodyParser = require("body-parser"),
    axios = require("axios"),
    mongoose = require("mongoose"),
    flash = require("connect-flash"),
    fs = require('fs'),
    multer = require("multer"),
    path = require('path'),
    app = express();

app.use('/uploads', express.static(path.join(__dirname, '/uploads')));

const storage = multer.diskStorage({
    destination: (req, file, cb) => {
        cb(null, 'uploads');
    },
    filename: (req, file, cb) => {
        console.log(file);
        cb(null, Date.now() + ".jpg");
    }
});
const fileFilter = (req, file, cb) => {
    if (file.mimetype == 'image/jpeg' || file.mimetype == 'image/png') {
        cb(null, true);
    } else {
        cb(null, false);
    }
}
const upload = multer({ storage: storage, fileFilter: fileFilter });

app.use(bodyParser.urlencoded({extended: true}));
app.set("view engine", "ejs");
app.use(express.static(__dirname + "/public"))


//HOME PAGE ROUTE
app.get("/", (req, res)=> {
    res.render("home")
})

//TEST ROUTES
app.get("/test", (req, res) => {
    res.render("form", {data1: null})
})

app.post("/test", upload.single('image'), function(req, res, next) {
    const spawn = require("child_process").spawn;
    const datax = [];
    var process = spawn('python',["./app.py",
        req.query.firstname,
        req.query.lastname] );
    process.stdout.on('data', function(data) {
        datax.push(data)
    })
    process.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        fs.readFile("prediction.json", (err, data1) => {
            data1 = JSON.parse(data1)
            res.render("form", {data1: data1})
        })
    })
})

app.listen(port, () => {
    console.log("Server started")
})

