def leaderboard():
	polls={}
	for user in user_auth.objects.all():
		polls.append({global.user.user_name:user.points})
	return polls
