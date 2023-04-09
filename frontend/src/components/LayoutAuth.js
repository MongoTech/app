import React from 'react';
import HeaderAuth from './HeaderAuth';
import {Route, Switch} from "react-router-dom";
import Login from '../pages/auth/login'
import Signup from '../pages/auth/signup'
import Forgot from '../pages/auth/forgot'
import Reset from '../pages/auth/reset'
import Check from '../pages/auth/check'
import Inactive from '../pages/auth/inactive'
import Start from '../pages/start'
export default function Layout({ children }) {
  return (
    <>
      <HeaderAuth />
        <Switch>
            <Route path="/login"><Login/></Route>
            <Route path="/signup"><Signup/></Route>
            <Route path="/forgot"><Forgot/></Route>
            <Route path="/reset"><Reset/></Route>
            <Route path="/check"><Check/></Route>
            <Route exact path="/"><Start/></Route>
            <Route path="/inactive"><Inactive/></Route>
        </Switch>
      {children}
    </>
  );
}
