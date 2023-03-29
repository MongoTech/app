import {createSlice} from "@reduxjs/toolkit";


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
        }
    }
})

export const { addUser } = userSlice.actions
export default userSlice.reducer