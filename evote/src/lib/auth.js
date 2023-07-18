export const Authorization = process.env.REACT_APP_AUTH_TOKEN

export const apiHost = process.env.REACT_APP_SITE_URL

export const FetchWrapper = async (params) => {
    let _defaultHeaders = {
        "Content-Type": 'application/json',
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "X-Requested-With",
        Authorization

    }
    try {
        let response = await fetch(String(`${apiHost}${params.url}`), {
            headers: _defaultHeaders,
            method: params.method ? String(params.method) : 'GET',
            ...(params.method !== 'GET') && { body: String(params.data) }
        })
        let responseJSON = await response.json()
        let res = {
            status: "success",
            statusText: response.statusText,
            data: responseJSON
        }
        return res
    } catch (error) {
        console.error(error)
        let res = {
            statusText: "FetChWrapper: server error",
            status: "error",
            error: error
        }
        console.error(error)
        return res
    }

}