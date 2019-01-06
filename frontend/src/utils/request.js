import axios from 'axios'
import { Message, MessageBox} from 'element-ui'
import store from '@/store'
// import { getToken } from '@/utils/auth'

// create an axios instance
const service = axios.create({
  baseURL: process.env.BASE_API, // api 的 base_url
  timeout: 5000 // request timeout,
})

// request interceptor
service.interceptors.request.use(
  config => {
    // Do something before request is sent
    // if (store.getters.token) {
    //   // 让每个请求携带token-- ['X-Token']为自定义key 请根据实际情况自行修改
    //   config.headers['X-Token'] = getToken()
    // }
    console.log('#request is', config)
    return config
  },
  error => {
    // Do something with request error
    console.log(error) // for debug
    Promise.reject(error)
  }
)

// response interceptor
service.interceptors.response.use(
  response => response,
  response => {
    console.log('#response', response.response)
    const res = response
    if (res.response.status !== 200 && res.response.status !== 201) {
      let error_message = ''
      for (var error_key in res.response.data) {
        // check if the property/key is defined in the object itself, not in parent
        if (res.response.data.hasOwnProperty(error_key))
            error_message += error_key + ': ' + res.response.data[error_key] + '\n'
      }
      MessageBox.alert(error_message, {
        type: 'error',
      })
      console.log(error_message)
      return Promise.reject('error')
    } 
    else {
      return res.response.data
     }
  },
  error => {
    console.log('err' + error) // for debug
    Message({
      message: error.message,
      type: 'warning',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export default service
