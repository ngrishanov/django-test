<template>
  <div class="p-4">
    <h1 class="font-sans text-3xl text-center">Решение задач на код</h1>

    <div class="flex mt-4 -mx-4">
      <div class="w-1/2 px-2">
        <codemirror :value="functionCode" :options="cmOptions" @input="onCmCodeChange"></codemirror>
      </div>
      <div class="w-1/2 px-2">
        <p class="mb-4"><b>Задача:</b> напишите метод, суммирующий два числа a и b.</p>
        <p class="mb-4">
          <span class="text-gray-500" v-if="!status || status === STATUSES.EVALUATION">
            Здесь появится результат проверки
          </span>
          <span v-if="status === STATUSES.WRONG"><b>Результат:</b> неверно</span>
          <span v-if="status === STATUSES.CORRECT"><b>Результат:</b> верно</span>
        </p>
        <button
          class="btn"
          v-bind:class="{'btn-disabled': status === STATUSES.EVALUATION || !functionCode}"
          @click="sendSubmission"
        >
          <span v-if="status === STATUSES.EVALUATION"><i class="c-inline-spinner"></i>Проверяется...</span>
          <span v-else>Отправить</span>
        </button>
      </div>
    </div>

  </div>
</template>

<script>
const DEFAULT_CODE = `function sumTwoNumbers(a, b) {
  return 42
}
`

const STATUSES = {
  EVALUATION: 'evaluation',
  CORRECT: 'correct',
  WRONG: 'wrong',
}

const POLL_INTERVAL = 2000

const storedFunctionCode = window.localStorage.getItem('function_code')
const storedStatus = window.localStorage.getItem('status')

export default {
  name: 'Main',
  mounted() {
    const uuid = window.localStorage.getItem('uuid')

    if (uuid) {
      this.getSubmissionStatus()
    }
  },
  data() {
    return {
      functionCode: storedFunctionCode ? storedFunctionCode : DEFAULT_CODE,
      status: storedStatus ? storedStatus : null,
      STATUSES: STATUSES,
    }
  },
  computed: {
    cmOptions() {
      return {
        tabSize: 4,
        mode: 'text/javascript',
        theme: 'base16-dark',
        lineNumbers: true,
        line: true,
        readOnly: this.status === this.STATUSES.EVALUATION ? 'nocursor' : false
      }
    }
  },
  methods: {
    sendSubmission() {
      window.localStorage.setItem('function_code', this.functionCode)

      fetch(
        '/api/submissions/',
        {
          method: 'POST',
          body: JSON.stringify({function_code: this.functionCode})
        }
      )
      .then(response => response.json())
      .then(data => {
        window.localStorage.setItem('uuid', data.result.uuid)

        this.status = data.result.status
        window.localStorage.setItem('status', this.status)

        this.getSubmissionStatus()
      })
    },
    getSubmissionStatus() {
      const uuid = window.localStorage.getItem('uuid')

      if (!uuid) {
        return
      }

      fetch(`/api/submissions/${uuid}/`)
      .then(response => response.json())
      .then(data => {
        this.status = data.result.status
        window.localStorage.setItem('status', this.status)

        if (this.status === this.STATUSES.EVALUATION) {
          setTimeout(this.getSubmissionStatus, POLL_INTERVAL)
        } else {
          window.localStorage.removeItem('uuid')
        }
      })
    },
    onCmCodeChange(newCode) {
      this.functionCode = newCode
    }
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<!-- spinner styles from https://codepen.io/vovchisko/pen/vROoYQ -->
<style scoped>
.btn {
  @apply bg-blue-500 text-white font-bold py-2 px-4 rounded;
}

.btn-disabled {
  @apply opacity-50 cursor-not-allowed;
  pointer-events: none;
}

@keyframes c-inline-spinner-kf {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.c-inline-spinner,
.c-inline-spinner:before {
  display: inline-block;
  width: 16px;
  height: 16px;
  transform-origin: 50%;
  border: 2px solid transparent;
  border-color: #e7f5ff #e7f5ff transparent transparent;
  border-radius: 50%;
  content: "";
  animation: linear c-inline-spinner-kf 900ms infinite;
  position: relative;
  vertical-align: inherit;
  line-height: inherit;
}

.c-inline-spinner {
  top: 2px;
  margin: 0 8px 0 2px;
}

.c-inline-spinner:before {
  border-color: #e7f5ff #e7f5ff transparent transparent;
  position: absolute;
  left: -2px;
  top: -2px;
  border-style: solid;
}
</style>
