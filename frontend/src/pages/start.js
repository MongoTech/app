import Button from 'react-bootstrap/Button';
import Modal from 'react-bootstrap/Modal';
import {useHistory} from "react-router-dom";
import {getToken} from "../services/token";
import Google from '../components/Googel'
export default function Start() {
    const history = useHistory()
    if (getToken()) {
        window.location.href = "/dashboard"
    }
    return <>
        <div
            className="modal show"
            style={{display: 'block', position: 'initial'}}
        >
            <Modal.Dialog show={false}>
                <Modal.Header closeButton>
                    <img src="https://mongo.one/img/icons/logo.svg" alt="Logo" />
                </Modal.Header>

                <Modal.Body>
                    <p>You can login or signup</p>
                    <Google />
                </Modal.Body>

                <Modal.Footer>
                    <Button variant="secondary" onClick={()=>{history.push("/login")}}>Login</Button>
                    <Button variant="primary" onClick={()=>{history.push("/signup")}}>SignUp</Button>
                </Modal.Footer>
            </Modal.Dialog>

        </div>
    </>
}