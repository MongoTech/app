import withToken from "../../hocs/withToken";
import Inactive from "../../components/pages/auth/inactive";
import {getToken} from "../../services/token";
import {useHistory} from "react-router-dom";
import { useSelector } from "react-redux";

const InactivePage = () =>{
    const user = useSelector((state)=>state)
    const history = useHistory()
    if (getToken() && user.is_active) {
        history.push("/dashboard")
    }
    return <Inactive />
}

export default withToken(InactivePage)