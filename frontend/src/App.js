import React, { Component } from 'react'
import Instructions from './Instructions'
import Contact from './Contact'
import Counter from "./Counter"

class App extends Component {
  constructor(props) {
    super(props)
    this.counter = React.createRef()
    this.state = {
      contacts: [
        {id: 1, name: "Angad", nickname: "greg", hobby: "dirty-ing"},
        {id: 2, name: "Roy", nickname: "uwu", hobby: "weeb"},
        {id: 3, name: "Daniel", nickname: "oppa", hobby: "losing money with options trading"},
      ]
    }
  }
  handleSubmit = event => {
    event.preventDefault()
    this.counter.current.handleInc()
    let new_contact = {id: this.state.contacts.length+1, name: this.nodeName.value, nickname: this.nodeNickname.value, hobby: this.nodeHobby.value}
    let updated_contacts = this.state.contacts;
    updated_contacts.push(new_contact)
    console.log(updated_contacts);
    this.setState({contacts: updated_contacts});
    this.nodeForm.reset()
  }
  render() {
    return (
      <div className="App">
        <Instructions complete="true"/>
        <Counter ref={this.counter}/>
        <br />
        <form onSubmit={this.handleSubmit} ref={node => (this.nodeForm = node)}>
        <label>Name:
          <input type="text" ref={node => (this.nodeName = node)}/>
        </label> <br />
        <label>Nickname:
          <input type="text" ref={node => (this.nodeNickname = node)}/>
        </label> <br />
        <label>Hobby:
          <input type="text" ref={node => (this.nodeHobby = node)}/>
        </label> <br />
        <button type="submit">Submit</button>
      </form>
        <br />
        {this.state.contacts.map(x => (
          <Contact id={x.id} name={x.name} nickname={x.nickname} hobby={x.hobby} />
        ))}
      </div>
    )
  }
}

export default App
