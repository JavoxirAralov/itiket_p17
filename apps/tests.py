class Task(CreatedBaseModel, TranslatableModel):
    translations = TranslatedFields(
        title=CharField(_('title'), max_length=255),
        description=CharField(_('description'), max_length=255),
        status=CharField(_('status'), max_length=255),
        user_task_list=CharField(_('user_task_list'), max_length=255)
    )
    lesson = ForeignKey('apps.Lesson', CASCADE)
    task_number = PositiveIntegerField(default=0)
    lastTime = DateTimeField()
    order = IntegerField()
    priority = PositiveIntegerField(default=0)
    mustComplete = BooleanField()
    files = CharField(max_length=255)

    class Meta:
        verbose_name = _('Task')
        verbose_name_plural = _('Task')

    def __str__(self):
        return self.lesson.title