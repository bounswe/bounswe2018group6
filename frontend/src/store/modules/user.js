import { loginByUsername, getUserInfo, signupDate } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { MessageBox } from 'element-ui'

const user = {
  state: {
    user: '',
    status: '',
    code: '',
    token: getToken(),
    user_id: -1,
    is_corporate_user: null,
    corporate_profile: '',
    follower_count: 0,
    following_count: 0,
    owner_events_count: 0,
    name: '',
    avatar: '',
    introduction: '',
    roles: [],
    setting: {
      articlePlatform: []
    }
  },

  mutations: {
    SET_CODE: (state, code) => {
      state.code = code
    },
    SET_USER_ID: (state, user_id) => {
      state.user_id = user_id
    },
    SET_USERNAME: (state, username) => {
      state.username = username
    },
    SET_TOKEN: (state, token) => {
      state.token = token
    },
    SET_INTRODUCTION: (state, introduction) => {
      state.introduction = introduction
    },
    SET_SETTING: (state, setting) => {
      state.setting = setting
    },
    SET_STATUS: (state, status) => {
      state.status = status
    },
    SET_FIRSTNAME: (state, first_name) => {
      state.first_name = first_name
    },
    SET_LASTNAME: (state, last_name) => {
      state.last_name = last_name
    },
    SET_AVATAR: (state, avatar) => {
      state.avatar = avatar
    },
    SET_FOLLOWER: (state, follower_count) => {
      state.follower_count = follower_count
    },
    SET_FOLLOWING: (state, following_count) => {
      state.following_count = following_count
    },
    SET_OWNER_EVENT: (state, owner_events_count) => {
      state.owner_events_count = owner_events_count
    },
    SET_TAGS: (state, tags) => {
      state.tags = tags
    },
    SET_ROLES: (state, roles) => {
      state.roles = roles
    }
  },

  actions: {
    LoginByUsername({ commit }, userInfo) {
      const username = userInfo.username.trim()
      return new Promise((resolve, reject) => {
        loginByUsername(username, userInfo.password).then(response => {
          const data = response.data
          commit('SET_TOKEN', data.token)
          setToken(response.data.token)
          commit('SET_USER_ID', data.user_id)
          commit('SET_USERNAME', username)
          resolve()
        }).catch(error => {
          MessageBox.alert('Sorry. Check your username or password!', {
            type: 'warning'
          })
          reject(error)
        })
      })
    },

    signupDate({ commit }, user) {
      const username = user.username.trim()
      return new Promise((resolve, reject) => {
        signupDate(user.first_name, user.last_name, user.email, username, user.password, user.is_corporate_user, user.corporate_profile).then(response => {
          const data = response.data
          commit('SET_USER_ID', data.id)
          resolve()
        }).catch(error => {
          MessageBox.alert('This username or email is used. Please, enter new one!', {
            type: 'warning'
          })
          reject(error)
        })
      })
    },

    GetUserInfo({ commit, state }) {
      return new Promise((resolve, reject) => {
        getUserInfo(state.user_id).then(response => {
          console.log('#data', data)
          if (!response.data) { // 由于mockjs 不支持自定义状态码只能这样hack
            reject('error')
          }
          const data = response.data
          data.roles = ['admin']
          if (data.roles && data.roles.length > 0) { // 验证返回的roles是否是一个非空数组
            commit('SET_ROLES', data.roles)
          } else {
            reject('getInfo: roles must be a non-null array !')
          }
          commit('SET_FIRSTNAME', data.first_name)
          commit('SET_LASTNAME', data.last_name)
          commit('SET_AVATAR', data.avatar)
          commit('SET_FOLLOWER', data.follower_count)
          commit('SET_FOLLOWING', data.following_count)
          commit('SET_TAGS', data.tags)
          resolve(response)
        }).catch(error => {
          reject(error)
        })
      })
    },

    // 第三方验证登录
    // LoginByThirdparty({ commit, state }, code) {
    //   return new Promise((resolve, reject) => {
    //     commit('SET_CODE', code)
    //     loginByThirdparty(state.status, state.email, state.code).then(response => {
    //       commit('SET_TOKEN', response.data.token)
    //       setToken(response.data.token)
    //       resolve()
    //     }).catch(error => {
    //       reject(error)
    //     })
    //   })
    // },

    // 登出
    LogOut({ commit, state }) {
      commit('SET_TOKEN', '')
      commit('SET_ROLES', [])
      removeToken()

      // return new Promise((resolve, reject) => {
      //   logout(state.token).then(() => {
      //     commit('SET_TOKEN', '')
      //     commit('SET_ROLES', [])
      //     removeToken()
      //     resolve()
      //   }).catch(error => {
      //     reject(error)
      //   })
      // })
    },

    // 前端 登出
    FedLogOut({ commit }) {
      return new Promise(resolve => {
        commit('SET_TOKEN', '')
        removeToken()
        resolve()
      })
    },

    // 动态修改权限
    ChangeRoles({ commit, dispatch }, role) {
      return new Promise(resolve => {
        commit('SET_TOKEN', role)
        setToken(role)
        getUserInfo(role).then(response => {
          const data = response.data
          commit('SET_ROLES', data.roles)
          commit('SET_NAME', data.name)
          commit('SET_AVATAR', data.avatar)
          commit('SET_INTRODUCTION', data.introduction)
          dispatch('GenerateRoutes', data) // 动态修改权限后 重绘侧边菜单
          resolve()
        })
      })
    }
  }
}

export default user
