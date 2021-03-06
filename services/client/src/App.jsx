import React, { Component } from 'react';
import axios from 'axios';
import { Route, Switch } from 'react-router-dom';

import UsersList from './components/UsersList';
import About from './components/About';
import NavBar from './components/NavBar';
import Form from './components/Form';
import Logout from './components/Logout';
import UserStatus from './components/UserStatus';

class App extends Component {
  constructor() {
    super();
    this.state = {
      users: [],
      username: '',
      email: '',
      title: 'TestDriven.io',
      formData: {
        username: '',
        email: '',
        password: ''
      },
      isAuthenticated: false,
      error: false
    };
    this.handleChange = this.handleChange.bind(this);
    this.handleFormChange = this.handleFormChange.bind(this);
    this.handleUserFormSubmit = this.handleUserFormSubmit.bind(this);
    this.logoutUser = this.logoutUser.bind(this);
  }
  componentDidMount() {
    this.getUsers();
  }
  getUsers() {
    axios
      .get(`${process.env.REACT_APP_USERS_SERVICE_URL}/users`)
      .then(res => {
        this.setState({ users: res.data.data.users });
      })
      .catch(err => {
        console.log(err);
      });
  }
 
  handleChange(event) {
    const obj = {};
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  }

  handleUserFormSubmit(event) {
    event.preventDefault();
    const formType = window.location.href.split('/').reverse()[0];
    let data = {
      email: this.state.formData.email,
      password: this.state.formData.password
    };
    if (formType === 'register') {
      data.username = this.state.formData.username;
    }
    const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/${formType}`;
    axios
      .post(url, data)
      .then(res => {
        this.setState({
          formData: { username: '', email: '', password: '' },
          username: '',
          email: '',
          isAuthenticated: true,
          error:false,
        });
        window.localStorage.setItem('authToken', res.data.auth_token);
        this.getUsers();
      })
      .catch((error) => {
        this.setState({ error: error.response.data.message});
      });
  }

  handleFormChange(event) {
    const obj = this.state.formData;
    obj[event.target.name] = event.target.value;
    this.setState(obj);
  }

  logoutUser() {
    window.localStorage.clear();
    this.setState({ isAuthenticated: false });
  }

  render() {
    return (
      <div>
        <NavBar
          title={this.state.title}
          isAuthenticated={this.state.isAuthenticated}
        />
        <div className="container">
          <div className="row">
            <div className="col-md-6">
              <br />
              <Switch>
                <Route
                  exact
                  path="/"
                  render={() => <UsersList users={this.state.users} />}
                />
                <Route exact path="/about" component={About} />
                <Route
                  exact
                  path="/register"
                  render={() => (
                    <Form
                      formType={'Register'}
                      formData={this.state.formData}
                      error={this.state.error}
                      handleFormChange={this.handleFormChange}
                      handleUserFormSubmit={this.handleUserFormSubmit}
                      isAuthenticated={this.state.isAuthenticated}
                    />
                  )}
                />
                <Route
                  exact
                  path="/login"
                  render={() => (
                    <Form
                      formType={'Login'}
                      formData={this.state.formData}
                      error={this.state.error}
                      handleFormChange={this.handleFormChange}
                      handleUserFormSubmit={this.handleUserFormSubmit}
                      isAuthenticated={this.state.isAuthenticated}
                    />
                  )}
                />
                <Route
                  exact
                  path="/logout"
                  render={() => (
                    <Logout
                      logoutUser={this.logoutUser}
                      isAuthenticated={this.state.isAuthenticated}
                    />
                  )}
                />
                <Route
                  exact
                  path="/status"
                  render={() => (
                    <UserStatus isAuthenticated={this.state.isAuthenticated} />
                  )}
                />
              </Switch>
            </div>
          </div>
        </div>
      </div>
    );
  }
}

export default App;
