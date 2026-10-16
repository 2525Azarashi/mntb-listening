import { subjectDefinitionOf } from '../data/subjects';
import type { SubjectKey } from '../data/allChapters';
import { getChapterIndexOfSubject } from '../data/chapterIndex.generated';

/** Learning entry only; battle remains available from the existing main navigation. */
export function studyEntry(subject: SubjectKey): 'chapters' | 'mode_selection' {
  return subjectDefinitionOf(subject)?.entry ?? 'chapters';
}

export function isLearningScreen(screen: string): boolean {
  // 'study'（演習する：科目・コンテンツ選択）と 'foundation'（英単語・聞き取りの文法）も「学習」の画面
  return ['study', 'foundation', 'mode_selection', 'advanced_fields', 'chapters', 'learning', 'quiz', 'explanation', 'mock_exam'].includes(screen);
}

export function safeStudyResume(subject: SubjectKey, screen: string, chapterId: string | null): string {
  if (!isLearningScreen(screen)) return studyEntry(subject);
  if (['quiz', 'explanation'].includes(screen) &&
      !getChapterIndexOfSubject(subject).some(chapter => chapter.id === chapterId)) {
    return studyEntry(subject);
  }
  // 旧版の画面（化学の分野選択・予想問題）が保存されていたら、入口へ戻す
  if (screen === 'advanced_fields' || screen === 'mock_exam') return studyEntry(subject);
  if (screen === 'learning' && studyEntry(subject) === 'chapters') return 'chapters';
  return screen;
}
