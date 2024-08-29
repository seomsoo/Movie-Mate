<template>
  <div>
    <div class="modal fade" id="movieModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" @shown.bs.modal="onModalShown">
      <div class="modal-dialog">
        <div class="modal-content modal-box">
          <div class="modal-header">
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <iframe :src="iframeUrl" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  movie: Object,
  trailer: String
})

const iframeUrl = ref('')

const updateIframeUrl = () => {
  iframeUrl.value = `https://www.youtube.com/embed/${props.trailer}?autoplay=1`
}

const onModalShown = () => {
  updateIframeUrl()
}

// Ensure to call updateIframeUrl initially to set the URL when the component is mounted
updateIframeUrl()
</script>

<style scoped>
.modal-box {
  max-width: 800px; /* 원하는 크기로 수정 */
  width: 100%;
  border-radius: 10px; /* 모서리 둥글게 */
  overflow: hidden;
}

.modal-header {
  background-color: #000000; /* 헤더 배경색 */
  color: white; /* 텍스트 색상 */
  border-bottom: none; /* 경계선 제거 */
}

.modal-header .btn-close {
  background: none;
  border: none;
  color: white;
  font-size: 1.2rem;
  cursor: pointer;
}

.modal-header .btn-close:hover {
  color: #ff0000;
}

.modal-body {
  padding: 0; /* 여백 제거 */
  background-color: #000; /* 배경색 */
}

iframe {
  width: 100%;
  height: 450px; /* 원하는 높이로 수정 */
  border: none;
  border-radius: 0 0 10px 10px; /* 아래쪽 모서리 둥글게 */
}
</style>
