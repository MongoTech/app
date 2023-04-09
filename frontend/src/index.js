import React from 'react';
import {createRoot} from 'react-dom/client';
import {transitions, positions, Provider as AlertProvider} from 'react-alert'
import AlertTemplate from 'react-alert-template-basic'
import {store} from "./store"
import {Provider} from "react-redux";
import {BrowserRouter, Route, Switch, useParams} from "react-router-dom";
import Layout from "./components/Layout";
import {getToken} from "./services/token";
import LayoutAuth from "./components/LayoutAuth";
import './assets/css/ionicons.min.css';
import './assets/scss/style.scss';
import 'bootstrap/dist/css/bootstrap.min.css';


import Users from "./pages/users";
import UsersNew from "./pages/users/new";
import UsersEdit from "./pages/users/edit";

import Dashboard from "./pages/dashboard";

const options = {
    position: positions.TOP_CENTER,
    timeout: 5000,
    offset: "100px",
    type: "error",
    transition: transitions.FADE
}


const root = createRoot(document.getElementById('root'))
root.render(
    <React.StrictMode>
        <AlertProvider template={AlertTemplate} {...options}>
            <Provider store={store}>
                <BrowserRouter>
                    <Layout />
                </BrowserRouter>
            </Provider>
        </AlertProvider>
    </React.StrictMode>,
);

