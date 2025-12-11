Permission behaviour summary
PostCreateView uses LoginRequiredMixin so only logged-in users can create posts.
PostUpdateView and PostDeleteView use LoginRequiredMixin + UserPassesTestMixin with test_func ensuring only the post author can edit or delete.
PostListView and PostDetailView are public.


Blog Post Management (CRUD)
- List: Public, url name 'blog:post_list' (root '/')
- Detail: Public, 'blog:post_detail' -> /posts/<pk>/
- Create: Requires login, 'blog:post_create' -> /posts/new/
- Update: Requires login and author ownership, 'blog:post_update' -> /posts/<pk>/edit/
- Delete: Requires login and author ownership, 'blog:post_delete' -> /posts/<pk>/delete/
Forms: blog/forms.py -> PostForm (title and content)
Permissions: LoginRequiredMixin and UserPassesTestMixin ensure secure actions.


#Permission & UI notes
comment_create is protected by @login_required, so anonymous users are prompted to log in.
CommentUpdateView and CommentDeleteView use UserPassesTestMixin to ensure only the comment author can edit/delete.
If you want moderators/admins to be able to delete any comment, change test_func in CommentAuthorRequiredMixin to allow request.user.is_staff or request.user.is_superuser.
Consider adding a small rate limit or spam protection if your site is public (e.g., simple throttle in view or using third-party packages).


#Documentation (short)
How to add a comment
Log in.
On a post detail page, use the “Leave a comment” box and submit. The comment is saved and appears under the post.
How to edit a comment
As the comment author, click “Edit” on your comment. Update and submit. Only the author (and staff, if you allow) can edit.
How to delete a comment
As the comment author, click “Delete” and confirm. Staff users can be given delete rights by allowing is_staff in the permission mixin.
URLs
Create comment: POST /posts/<post_id>/comments/new/ (login required)
Edit comment: /comments/<comment_pk>/edit/ (author only)
Delete comment: /comments/<comment_pk>/delete/ (author only)


Adding tags: In the post create/edit form there’s a tags input. Enter comma-separated tag names. New tags are created automatically.
Viewing posts by tag: Click a tag badge on a post or visit /tags/<tag_slug>/ to see posts with that tag.
Search: Use the search box (site header) or /search/?q=keyword to find posts whose title, content, or tags contain keyword.