import type { Interface } from "readline";
import type { DeviationSpamAnalysisResult } from "./type";
import type { Queue } from "./queue";

export interface IFTestPromptProcesser {
    collectionSize: number
    readline: Interface


    setMainSection(i: number): void
    displaySection({ messageTimestamps, epsilon, timeoutLimit, delays, repetitionScores }: DeviationSpamAnalysisResult ): void
}

export interface IFDeviationBaseSpammmingDetector {
    epsilon: number,
    timestampQueue: Queue<number>
    timeoutLimit: number // milli-seocnd https://currentmillis.com/

    collectTimestamp(timestamp: number): void
    getRepetitionScoreArray(): DeviationSpamAnalysisResult
    getDelayArray(): Array<number>
}

export interface IFQueue<T> { 
    put(data:T): IFQueue<T>
    get(): T | undefined
    display(): void
    asArray(): Array<T>
    clear(): Array<T>
}