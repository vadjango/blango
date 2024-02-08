class Greeter {
  constructor(name) {
    this.name = name;
  }
  getGreeting() {
    if (this.name === undefined) {
      return "Hello, no name"
    } else {
      return "Hello, " + this.name
    }
  }
  showGreeting(greetingMessage) {
    console.log(greetingMessage);
  }
  greet() {
    this.showGreeting(this.getGreeting())
  }
}

class DelayedGreeter extends Greeter {
  delay = 2000
  
  constructor(name, delay) {
    super(name);
    if (delay !== undefined) {
      this.delay = delay
    }
  }
  greet() {
    setTimeout(() => {
      this.showGreeting(this.getGreeting())
    }, this.delay);
  }
}

const noNameGreeter = new Greeter();
const namedGreeter = new Greeter("Vadim");

const delayedGreeter = new DelayedGreeter("Vasia")
const delayDefinedGreeter = new DelayedGreeter("Olia", 1000);
noNameGreeter.greet();
namedGreeter.greet();
delayedGreeter.greet();
delayDefinedGreeter.greet();
