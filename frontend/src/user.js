import {createSlice} from "@reduxjs/toolkit";
import { connect } from "react-redux";

const initialState = {
    full_name: "Full Name",
    email: "user@example.com",
    is_superuser: null,
    is_active: null,
}

const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        addUser: (state, {payload}) => {
            return ({
                full_name: payload.full_name,
                email: payload.email,
                is_superuser: payload.is_superuser,
                is_active: payload.is_active
            })
        },
        getState: (state) => {
            return state
        }
    }
})
const mapStateToProps = state => ({
    user: state.user // map state to props
  });
export const userData = connect(mapStateToProps)
export const { addUser, getState} = userSlice.actions
export default userSlice.reducer