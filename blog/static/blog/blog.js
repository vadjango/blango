class ClickButton extends React.Component {
  state = {
    wasClicked: false
  }

  handleClick() {
    this.setState({wasClicked: true})
  }
  render() {
    let buttonName;
    if (this.state.wasClicked) {
      buttonName = "Clicked";
    } else {
      buttonName = "Click me!";
    }
    return React.createElement(
      "button",
      {
        className: "btn btn-primary mt-2",
        onClick: () => {
          this.handleClick()
          }
      },
      buttonName
    )
  }
}

const domContainer = document.getElementById("react_root");
ReactDOM.render(
  React.createElement(ClickButton), 
  domContainer
);
