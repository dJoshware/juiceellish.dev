$(document).ready(function() {
    
    var canvas = document.querySelector('.dynamic');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    var c = canvas.getContext('2d');

    var colors = [
        '#375A7F',
        '#4D7CAE',
        '#6A99CB'
    ];

    window.addEventListener('resize', function() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        init();
    });

    // Utility Functions
    function randomIntFromRange(min, max) {
        return Math.floor(Math.random() * (max - min + 1) + min);
    }

    function randomColor(colors) {
        return colors[Math.floor(Math.random() * colors.length)];
    }

    function RainDrop(x, y, dx, dy, length, steepness, color) {
        this.x = x;
        this.y = y;
        this.dx = dx;
        this.dy = dy;
        this.length = length;
        this.steepness = steepness;
        this.color = color;

        this.angle = Math.PI / 4 + this.steepness;

        this.draw = function() {
            c.beginPath();
            c.moveTo(this.x, this.y);
            c.lineTo(this.x + this.length * Math.cos(this.angle), this.y + this.length * Math.sin(this.angle));
            c.lineWidth = 2;
            c.strokeStyle = this.color;
            c.stroke();
        }

        this.update = function() {
            if (this.y + this.length > canvas.height) {
                this.x = randomIntFromRange(0, canvas.width);
                this.y = 0;
            }
            if (this.x + this.length > canvas.width) {
                this.y = randomIntFromRange(0, canvas.height);
                this.x = 0;
            }
    
            this.x += this.dx;
            this.y += this.dy;

            this.draw();
        }

    }

    var rainArray = [];

    function init() {
        rainArray = []
        var steepness = Math.PI / 12;
        for (var i = 0; i < 4000; i++) {
            var x = randomIntFromRange(0, canvas.width);
            var y = randomIntFromRange(0, canvas.height);
            var dx = randomIntFromRange(3, 4) * 0.4;
            var dy = randomIntFromRange(4, 5);
            var length = randomIntFromRange(12, 17);
            var color = randomColor(colors);
            rainArray.push(new RainDrop(
                x, // x coordinate
                y, // y coordinate
                dx, // x velocity
                dy, // y velocity
                length, // object length
                steepness, // object angle
                color // object color
            ));
        }
    }

    function animate() {
        requestAnimationFrame(animate);
        c.clearRect(0, 0, canvas.width, canvas.height);

        for (var i = 0; i < rainArray.length; i++) {
            rainArray[i].update();
        }
    }

    init();
    animate();

});
