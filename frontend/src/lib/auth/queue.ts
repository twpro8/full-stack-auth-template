type QueueEntry = {
  resolve: (value?: unknown) => void
  reject: (reason?: unknown) => void
}

let queue: QueueEntry[] = []

export const addToQueue = (entry: QueueEntry) => {
  queue.push(entry)
}

export const processQueue = (error: Error | null) => {
  queue.forEach((entry) => (error ? entry.reject(error) : entry.resolve()))
  queue = [] // drain
}
