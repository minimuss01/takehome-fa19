import React, { Component } from 'react'

class Counter extends Component {
  // YOUR CODE GOES BELOW
  constructor(props) {
    super(props)
    this.state = {
      count: 0
    }
  }

  handleInc = () => {
    this.setState({count: this.state.count + 1})
  }
  handleDec = () => {
    this.setState({count: this.state.count - 1})
  }

  render() {
    return (
      <div>
        <p>Counter</p>
        <label>{this.state.count}</label>
        <br></br>
        <button onClick={this.handleInc}>Increment</button>
        <button onClick={this.handleDec}>Decrement</button>
      </div>
    )
  }
}

export default Counter
