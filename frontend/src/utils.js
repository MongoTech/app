const populateSelect = (data, label_field) => {
    let result = []
    for (const i in data) {
        if (typeof data[i] === "object") {
            result.push({value: data[i].id, label: data[i][label_field]})
        }
    }
    return result
}

const convertList = (list, field) => {
    let result = []
    for (const i in list) {
        if (list[i].created) {
            result[list[i].id] = list[i].created
        }
        if (list[i].full_name) {
            result[list[i].id] = list[i].full_name
        }

    }

    console.log(result)
    return result
}

const deleteRow = (id) => {
    const elements = document.getElementsByClassName("td" + id)
    for (const el in elements) {
        if (elements[el].style) {
            elements[el].style.color = "black"
            elements[el].style.backgroundColor = "red"
        }
    }
}
const showError = (alert, response) => {
    if (response.response) {
        let message = response.response.data.detail ? response.response.data.detail : response.response.data
        if (typeof message === "object") {
            console.log("Object")
            message = message[0]["msg"]
        }
        alert.show(message)
    } else if (response.message) {
        alert.show(response.message)
    }
    else {
        alert.show(response)
    }
}
const id2key = async (list) => {
    return Object.fromEntries((await list).map(item => [item.id, item]));
}
export {populateSelect, convertList, id2key, deleteRow, showError}