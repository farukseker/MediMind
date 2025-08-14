<template>
<section class="px-4 space-y-4 max-w-md mx-auto">
    <header>
        <button 
        @click="$router.back()"
        class="btn btn-ghost ps-0 text-xl">
            <font-awesome :icon="faArrowLeft" />
        </button>
        <h1 class="text-xl font-bold">Ayarlar</h1>
    </header>
    <article>
        <fieldset class="w-full fieldset shadow rounded-box p-2">
            <legend class="fieldset-legend font-bold">Kullanıcı ayarları</legend>
            <SettingsButton :icon="faUser" title="Kişisel bilgiler" to="/settings/personal_information" />
            <SettingsButton :icon="faKey" title="Şifre değiştir" to="/settings/change_password" />
        </fieldset>
    </article>
    <article>
        <fieldset class="w-full fieldset shadow rounded-box p-2">
            <legend class="fieldset-legend font-bold">Bildirim ayarları</legend>
            <SettingsButton 
                :icon="faBell"
                title="Bildirim ayarları"
                to="/settings/notification_settings" 
                description="Açık"
            />
        </fieldset>
    </article>
    <article>
        <fieldset class="w-full fieldset shadow rounded-box p-2">
            <legend class="fieldset-legend font-bold">Erişebilirlik ayarları</legend>
            <SettingsButton 
                :icon="faLanguage"
                title="Dil"
                to="/settings/change_language" 
                :description="locale.toUpperCase()"
            />
            <SettingsButton 
                :icon="faCircleHalfStroke"
                title="Tema"
                to="/settings/themes" 
                :description="themeStore.theme.toUpperCase().slice(0, 1).toUpperCase() + themeStore.theme.slice(1)"
            />
        </fieldset>
    </article>
    <article>
        <fieldset class="w-full fieldset shadow rounded-box p-2">
            <legend class="fieldset-legend font-bold">Destek ve Hakkında</legend>
            <SettingsButton :icon="faHeadset" title="Destek" to="/" />
            <SettingsButton :icon="faScroll" title="Hakkında" to="/" />
        </fieldset>
    </article>
    <article>
        <fieldset class="w-full fieldset shadow rounded-box p-2">
            <SettingsButton @click="logout" btnStyle="btn btn-ghost text-error" :icon="faDoorOpen" title="Çıkış yap" />
        </fieldset>
    </article>
    <article class="w-full flex justify-center">
        <a href="https://github.com/farukseker/MediMind/blob/main/project/verlog.md" target="_new" class="text-gray-400 text-xs font-semibold text-center mx-auto underline">Version. V0.01.01</a>
    </article>
</section>
</template>

<script setup>
import { 
    faHeadset,
    faArrowLeft,
    faLanguage,
    faUser,
    faKey,
    faDoorOpen,
    faScroll,
    faBell,
    faCircleHalfStroke
} from '@fortawesome/free-solid-svg-icons'
import { useLocaleRouter } from '~/composables/useLocaleRouter'

//color-scheme
const { go } = useLocaleRouter()
const { locale } = useI18n()

const accessToken = useCookie('access_token')
const refreshToken = useCookie('refresh_token')

const logout = () => {
  accessToken.value = ''
  refreshToken.value = ''
  go('/auth/login')
}

const themeStore = useThemeStore()

</script>