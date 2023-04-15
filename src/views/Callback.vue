<script lang="ts" setup>
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'

import { useGuard } from '@authing/guard-vue3'

const router = useRouter()

const guard = useGuard()

const handleAuthingLoginCallback = async () => {
  try {
    // 1. 触发 guard.handleRedirectCallback() 方法完成登录认证
    // 用户认证成功之后，我们会将用户的身份凭证存到浏览器的本地缓存中
    console.log('guard:', guard)
    console.log('try handleRedirectCallback')
    await guard.handleRedirectCallback()
    console.log('handleRedirectCallback finined')

    // 2. 处理完 handleRedirectCallback 之后，你需要先检查用户登录态是否正常
    // const loginStatus: JwtTokenStatus | undefined = await guard.checkLoginStatus()

    // console.log('checkLoginStatus, loginStatus:', loginStatus)
    // if (!loginStatus) {
    //   console.log('loginStatusInvalid, startWithRedirect')
    //   guard.startWithRedirect({
    //     scope: 'openid profile',
    //   })
    //   console.log('Redirect finished')
    //   return
    // }

    // // 3. 获取到登录用户的用户信息
    // const userInfo: User | null = await guard.trackSession()

    // console.log('jump to Root, userInfo:', userInfo)
    router.replace({
      name: 'Root',
    })
  }
  catch (e) {
    // 登录失败，推荐再次跳转到登录页面
    console.log('login Failed, try login again, error:', e)
    // guard.startWithRedirect({
    //   scope: 'openid profile',
    // })
  }
}

onMounted(() => {
  handleAuthingLoginCallback()
})
</script>

<template>
  <div class="callback-container" />
</template>
