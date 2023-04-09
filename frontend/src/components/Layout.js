import React from 'react';
import Header from './Header';
import {Route, Switch} from "react-router-dom";
import Dashboard from "../pages/dashboard";
import UsersEdit from "../pages/users/edit";
import UsersNew from "../pages/users/new";
import Users from "../pages/users";
import Login from "../pages/auth/login";
import Signup from "../pages/auth/signup";
import Forgot from "../pages/auth/forgot";
import Reset from "../pages/auth/reset";
import Check from "../pages/auth/check";
import Start from "../pages/start";
import Inactive from "../pages/auth/inactive";

export default function Layout({children}) {
    const notAuthorizedUrl = ["/login", "/signup", "/forgot", "/reset", "/check", "/"]
    return (
        <>{!notAuthorizedUrl.includes(window.location.pathname)  &&  <Header />}
            <Switch>
                <Route path="/dashboard"><Dashboard/></Route>
                <Route path="/users/edit/:id"><UsersEdit/></Route>
                <Route path="/users/new"><UsersNew/></Route>
                <Route path="/users"><Users/></Route>

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
