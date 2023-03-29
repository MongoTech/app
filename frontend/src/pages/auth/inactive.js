import withToken from "../../hocs/withToken";
import Inactive from "../../components/pages/auth/inactive";
import {getToken} from "../../services/token";
import {useHistory} from "react-router-dom";
import { useSelector } from "react-redux";
const userSelector = (state) => {
    // state.createSlice.user
}

const InactivePage = () =>{
    const user = useSelector(userSelector)
    console.log(user)

    const history = useHistory()
    if (getToken()) {
        history.push("/dashboard")
    }
    return <Inactive />
}

export default withToken(InactivePage)