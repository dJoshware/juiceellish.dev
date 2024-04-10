$(document).ready(function() {

    // Flow field script
    var canvas = document.querySelector('.dynamic');
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    var c = canvas.getContext('2d');

    window.addEventListener('resize', function() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        initRain();
        initSnow();
    });

    class Particle {
        constructor(effect) {
            this.effect = effect;
            this.x = Math.floor(Math.random() * this.effect.width);
            this.y = Math.floor(Math.random() * this.effect.height);
            this.speedX;
            this.speedY;
            this.speedModifier = Math.floor(Math.random() * 3 + 1);
            this.history = [{x: this.x, y: this.y}];
            this.maxLength = Math.floor(Math.random() * 200 + 50);
            this.angle = 0;
            this.timer = this.maxLength * 2;
            this.colors = [
                '#F0D394',
                '#98651E',
                '#6E4B1F',
                '#533710'
            ];
            this.color = this.colors[Math.floor(Math.random() * this.colors.length)];
        }
        draw(context) {
            context.beginPath();
            context.moveTo(this.history[0].x, this.history[0].y);
            for (let i = 0; i < this.history.length; i++) {
                context.lineTo(this.history[i].x, this.history[i].y);
            }
            context.strokeStyle = this.color;
            context.stroke();
        }
        update() {
            this.timer--;
            if (this.timer >= 1) {
                let x = Math.floor(this.x / this.effect.cellSize);
                let y = Math.floor(this.y / this.effect.cellSize);
                let index = y * this.effect.cols + x;
                this.angle = this.effect.flowField[index];

                this.speedX = Math.cos(this.angle);
                this.speedY = Math.sin(this.angle);
                this.x += this.speedX * this.speedModifier;
                this.y += this.speedY * this.speedModifier;

                this.history.push({x: this.x, y: this.y});
                if (this.history.length > this.maxLength) {
                    this.history.shift();
                }
            } else if (this.history.length > 1) {
                this.history.shift();
            } else {
                this.reset();
            }
        }
        reset() {
            this.x = Math.floor(Math.random() * this.effect.width);
            this.y = Math.floor(Math.random() * this.effect.height);
            this.history = [{x: this.x, y: this.y}];
            this.timer = this.maxLength * 2;
        }
    }

    class Effect {
        constructor(width, height) {
            this.width = width;
            this.height = height;
            this.particles = [];
            this.numberOfParticles = 1000;
            this.cellSize = 20;
            this.rows;
            this.cols;
            this.flowField = [];
            this.curve = 2;
            this.zoom = 0.08;
            this.init();
        }
        init() {
            // create flow field
            this.rows = Math.floor(this.height / this.cellSize);
            this.cols = Math.floor(this.width / this.cellSize);
            this.flowField = [];
            for (let y = 0; y < this.rows; y++) {
                for (let x = 0; x < this.cols; x++) {
                    let angle = (Math.cos(x * this.zoom) + Math.sin(y * this.zoom)) * this.curve;
                    this.flowField.push(angle);
                }
            }

            // create particles
            for (let i = 0; i < this.numberOfParticles; i++) {
                this.particles.push(new Particle(this));
            }
        }
        render(context) {
            // this.drawGrid(context);
            this.particles.forEach(particle => {
                particle.draw(context);
                particle.update();
            });
        }
    }

    var effect = new Effect(canvas.width, canvas.height);

    function animateFlow() {
        c.clearRect(0, 0, canvas.width, canvas.height);
        effect.render(c);
        requestAnimationFrame(animateFlow);
    }


    // Rain script
    var rainColors = [
        '#375A7F',
        '#4D7CAE',
        '#6A99CB'
    ];

    // Utility Functions for rain & snow
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

    function initRain() {
        rainArray = []
        var steepness = Math.PI / 12;
        for (var i = 0; i < 4000; i++) {
            var x = randomIntFromRange(0, canvas.width);
            var y = randomIntFromRange(0, canvas.height);
            var dx = randomIntFromRange(3, 4) * 0.4;
            var dy = randomIntFromRange(4, 5);
            var length = randomIntFromRange(12, 17);
            var color = randomColor(rainColors);
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

    function animateRain() {
        requestAnimationFrame(animateRain);
        c.clearRect(0, 0, canvas.width, canvas.height);

        for (var i = 0; i < rainArray.length; i++) {
            rainArray[i].update();
        }
    }


    // Snow script
    var snowColors = [
        '#F4F4F2',
        '#E8E8E8',
        '#BBBFCA'
    ];

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

    function initSnow() {
        circleArray = []
        for (var i = 0; i < 3000; i++) {
            var x = randomIntFromRange(0, canvas.width + radius);
            var y = randomIntFromRange(0, canvas.height + radius);
            var dx = randomIntFromRange(2, 3) * 0.2;
            var dy = randomIntFromRange(3, 4) * 0.4;
            var radius = randomIntFromRange(1, 2);
            var color = randomColor(snowColors);
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

    function animateSnow() {
        requestAnimationFrame(animateSnow);
        c.clearRect(0, 0, canvas.width, canvas.height);

        for (var i = 0; i < circleArray.length; i++) {
            circleArray[i].update();
        }
    }


    // Function to initialize selected animation
    function initAnimation(animationType) {
        switch (animationType) {
            case 'flow':
                animateFlow();
                break;
            case 'rain':
                initRain();
                animateRain();
                break;
            case 'snow':
                initSnow();
                animateSnow();
                break;
            default:
                // Do nothing
        }
    }

    // Function to start canvas animations upon selection
    $('.dropdown-item').click(function(e) {
        e.preventDefault();
        var selectedAnimation = $(this).attr('id');
        initAnimation(selectedAnimation);
    });

    // Function to validate form submission
    const regex = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    $('#form-submit').on('click', function(e) {
        e.preventDefault();
        const formName = $('.contact-form-name'),
            formEmail = $('.contact-form-email'),
            formMessage = $('.contact-form-message'),
            nameValue = formName.val(),
            emailValue = formEmail.val(),
            messageValue = formMessage.val(),
            errorName = $('.form-error-name'),
            errorEmail = $('.form-error-email'),
            errorMessage = $('.form-error-message');

        let a = false,
            b = false,
            c = false;

        if (nameValue) {
            a = true;
            formName.removeClass('input-error');
            errorName.css('display', 'none');
        } else {
            formName.addClass('input-error');
            errorName.css('display', 'block');
        }

        if (regex.test(emailValue)) {
            b = true;
            formEmail.removeClass('input-error');
            errorEmail.css('display', 'none');
        } else {
            formEmail.addClass('input-error');
            errorEmail.css('display', 'block');
        }

        if (messageValue) {
            c = true;
            formMessage.removeClass('input-error');
            errorMessage.css('display', 'none');
        } else {
            formMessage.addClass('input-error');
            errorMessage.css('display', 'block');
        }

        if (a && b && c) {
            $('.contact-form').submit();
            setTimeout(() => {
                $('.contact-form').trigger('reset');
            }, 1500);
        }
    });

    // Duplicate images in carousel to create loop effect
    $('.skills-slide').clone().appendTo('.skills');

    // Default particle animation
    $('#_default').click(function(e) {
        e.preventDefault();
        $('.canvas').attr('id', 'default');
    });

    // Highlight navbar sections as they're viewed
    const navItems = $('.nav_item');
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const targetId = entry.target.id;
                const correspondingNavItem = $(`#nav-${targetId}`);
                navItems.removeClass('nav_item_active');
                correspondingNavItem.addClass('nav_item_active');
            }
        });
    }, {
        root: null,
        rootMargin: '0px',
        threshold: .9
    });
    
    $('#hero, #about, #projects, #contact').each(function() {
        observer.observe(this);
    });

});
