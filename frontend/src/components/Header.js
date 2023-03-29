import React from 'react';
import {Link} from "react-router-dom";
import {Navbar, Nav, NavDropdown, Dropdown} from 'react-bootstrap';
import {deleteToken} from "../services/token";
import {getUserMe} from "../services/api";
import {useDispatch} from "react-redux";
import {addUser} from "../user"
import {useHistory} from "react-router-dom";
export default function Header() {
    const history = useHistory()
    const [full_name, setFullName] = React.useState()
    const [email, setEmail] = React.useState()
    const [user_id, setUserId] = React.useState()
    const [superuser, setSuperUser] = React.useState()
    const dispatch = useDispatch()

    React.useEffect(() => {
        const getUsersMe = async () => {
            let data = await getUserMe();
            dispatch(addUser(data))
            if (data) {
                if (data.is_active === false ) {
                    history.push("/inactive")
                }
                setFullName(data["full_name"])
                setEmail(data["email"])
                setUserId(data["id"])
                setSuperUser(data["is_superuser"])
            } else {
                deleteToken()
            }
        }

        getUsersMe().then()

    }, [dispatch])
    return (
        <>
            <Navbar expand="lg">
                <Link className="navbar-brand" to="/dashboard">
                    Home
                </Link>
                <Navbar.Toggle aria-controls="basic-navbar-nav"/>
                <Navbar.Collapse id="basic-navbar-nav">
                    <Nav className="navbar-nav">
                        {superuser ?
                        <NavDropdown title="Users">
                            <Link to="/users" className="dropdown-item">
                                List of users
                            </Link>
                            <Link to="/users/new" className="dropdown-item">
                                Add user
                            </Link>
                        </NavDropdown>:''}
                    </Nav>
                 <Nav className="navbar-nav text-right">
                            <Dropdown className="header-img-icon">
                                <Dropdown.Toggle variant="default">
                                    Profile
                                </Dropdown.Toggle>
                                <Dropdown.Menu>
                                    <div className="dropdown-header d-flex flex-column align-items-center">
                                        <div className="info text-center">
                                            <p className="name font-weight-bold mb-0">{full_name}</p>
                                            <p className="email text-muted mb-3">{email}</p>
                                        </div>
                                    </div>
                                    <div className="dropdown-body">
                                        <ul className="profile-nav">
                                            <li className="nav-item">
                                                <Link to="/profile" className="nav-link">
                                                    <i className="icon ion-md-person"></i>
                                                    <span>Profile</span>
                                                </Link>
                                            </li>
                                            <li className="nav-item">
                                                <Link to="/login" className="nav-link red" onClick={deleteToken}>
                                                    <i className="icon ion-md-power"></i>
                                                    <span>Log Out</span>
                                                </Link>
                                            </li>
                                        </ul>
                                    </div>
                                </Dropdown.Menu>
                            </Dropdown>
                        </Nav>
                </Navbar.Collapse>
            </Navbar>
        </>
    );
}
