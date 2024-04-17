$(document).ready(function() {
    
    var canvas = document.querySelector('.dynamic');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    var c = canvas.getContext('2d');

    var colors = [
        '#F4F4F2',
        '#E8E8E8',
        '#BBBFCA'
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

    function Circle(x, y, dx, dy, radius, color) {
        this.x = x;
        this.y = y;
        this.dx = dx;
        this.dy = dy;
        this.radius = radius;
        this.color = color;

        this.draw = function() {
            c.beginPath();
            c.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
            c.fillStyle = this.color;
            c.fill();
        }

        this.update = function() {
            if (this.y + this.radius > canvas.height) {
                this.x = randomIntFromRange(0, canvas.width);
                this.y = 0;
            }
            if (this.x + this.radius > canvas.width) {
                this.y = randomIntFromRange(0, canvas.height);
                this.x = 0;
            }
    
            this.x += this.dx;
            this.y += this.dy;

            this.draw();
        }

    }

    var circleArray = [];

    function init() {
        circleArray = []
        for (var i = 0; i < 3000; i++) {
            var x = randomIntFromRange(0, canvas.width + radius);
            var y = randomIntFromRange(0, canvas.height + radius);
            var dx = randomIntFromRange(2, 3) * 0.2;
            var dy = randomIntFromRange(3, 4) * 0.4;
            var radius = randomIntFromRange(1, 2);
            var color = randomColor(colors);
            circleArray.push(new Circle(
                x, // x coordinate
                y, // y coordinate
                dx, // x velocity
                dy, // y velocity
                radius, // object radius
                color // object color
            ));
        }
    }

    function animate() {
        requestAnimationFrame(animate);
        c.clearRect(0, 0, canvas.width, canvas.height);

        for (var i = 0; i < circleArray.length; i++) {
            circleArray[i].update();
        }
    }

    init();
    animate();

});
