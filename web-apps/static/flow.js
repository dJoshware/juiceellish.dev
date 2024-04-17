$(document).ready(function() {

    var canvas = document.querySelector('.dynamic');
    
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    var c = canvas.getContext('2d');

    c.fillStyle = 'white';
    c.strokeStyle = 'white';

    window.addEventListener('resize', function() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
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
                '#FAFAFA',
                '#C7EEFF',
                '#00B8FC',
                '#546373',
                // '#00B8FC',
                // '#8cdcfa',
                // '#2d7a96',
                // '#0582b0'
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
        // drawGrid(context) {
        //     for (let c = 0; c < this.cols; c++) {
        //         context.beginPath();
        //         context.moveTo(this.cellSize * c, 0);
        //         context.lineTo(this.cellSize * c, this.height);
        //         context.stroke();
        //     }
        //     for (let r = 0; r < this.rows; r++) {
        //         context.beginPath();
        //         context.moveTo(0, this.cellSize * r);
        //         context.lineTo(this.width, this.cellSize * r);
        //         context.stroke();
        //     }
        // }
        render(context) {
            // this.drawGrid(context);
            this.particles.forEach(particle => {
                particle.draw(context);
                particle.update();
            });
        }
    }

    var effect = new Effect(canvas.width, canvas.height);

    function animate() {
        c.clearRect(0, 0, canvas.width, canvas.height);
        effect.render(c);
        requestAnimationFrame(animate);
    }

    animate();

});
