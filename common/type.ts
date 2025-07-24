export type MessageTimestampElement = {
    timestamp: string; // UTC ms format
    message: string;
}

export type DeviationSpamAnalysisResult = {
    epsilon: number,
    timeoutLimit: number
    messageTimestamps: Array<number>,
    delays: Array<number>,
    repetitionScores: Array<number>,
}

export type MinMax = {
    "min": number,
    "max": number
} 