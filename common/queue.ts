import type { IFQueue } from "./interface";

export class Queue<T extends any> implements IFQueue<T> {
    private _queue!: Array<T>

    constructor() {
        this._queue = new Array<T>()
    }

    get size(): number {
        return this._queue.length
    };
    
    put(data: T): IFQueue<T> {
        this._queue.push(data)
        return this
    }

    get(): T | undefined {
        return this._queue.shift()
    }

    display(): void {
        let temp = new String("[ ")
        for(let i = 0; i < this._queue.length; i++) {
            
            if(this._queue.length-1 == i) {
                temp += `${this._queue[i]} ]`
            } else {
                temp += `${this._queue[i]}, `
            }
        }

        console.log(temp)
    }

    clear(): Array<T> {
        let temp = this._queue
        this._queue = []
        return temp
    }

    asArray(): T[] {
        return this._queue
    }
    
}
