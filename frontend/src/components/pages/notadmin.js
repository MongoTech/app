import {deleteToken} from "../services/token";
import {useHistory} from "react-router-dom";
export default function NotAdmin() {
    const history = useHistory()
    return <>You are not admin <button onClick={()=>{
    deleteToken()
    history.push("/")
    }
    }>logout</button></>
}